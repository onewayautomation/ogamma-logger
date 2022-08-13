# This project is built using materials from https://www.sqlitetutorial.net/sqlite-python/

import sqlite3
from sqlite3 import Error
import json
import os
import shutil

# Before running of the script, set test options below as required:

collectorConfigurationName = 'Test Configuration'
 
# Name of the SQLite database file where configuration is created. Required option.
# Can be existing file. If existing file, and recrteadeDb is true, then will be overritten by the souirce file. If recreateDb is false, then will be used as is.
# Note that if this file is configured to be used by OVL, then the OVL process must be stopped before and running this script.

# destinationDatabase = '../data/config.db'
destinationDatabase = '../docker/data/config.db'

# template database, which can be sued as a base. Optional. This can be empty database ot database with some settings already created.
sourceDatabase = './config-template.db'

# If true, and source database fiel exists, then destination file is overwrittem with copy of the source file.
# This is expected to be the case when this script runs multiple times, to prevent addning more records additionally to existing records.
recreateDb = False

# Hostname of the machine where OPC UA Server runs.
serverHostName = 'localhost'

# Ip address of the machine where OPC UA Server runs. This is used to resolve host name to IP address.
serverIpAddress = '127.0.0.1'

# Port number of the first OPC UA Server. Port number for other servers is incremented by one.
serverPortNumber=48010

# 3 means encrypted communication.
securityMode = 3 

# This json file goes into OPC UA Server configuration, Advanced Options
serverOptionsFileName = "./server-options.json"

# *******************************************************************************************************************
# Next few options define the load on the application
# Number of values collected per second is: numberOfServers * numberOfVariables * (1000.0/samplingInterval)
# *******************************************************************************************************************

# Number of Server connection nodes which wil be created in the Addsress Space panel.
numberOfServers = 5
		
# Logged variables per server
numberOfVariables = 100
samplingInterval=1000
publishingInterval=1000

# Function to get server advanced options:
def getServerJsonOptions(fileName, hostName = "", ipAddress = ""):
  f = open(fileName, "r")
  content = f.read()
  f.close()

  options = json.loads(content)

  # Add DNS resolution entry:
  if (len(hostName)>0 and len(ipAddress) >0 ):
    dnsRecord = {
      "from": hostName,
      "to": ipAddress
    }
    options["dnsMap"].append(dnsRecord)
  
  return json.dumps(options)


def createConnection(db_file):
  """ create a database connection to the SQLite database specified by db_file
  :param db_file: database file
  :return: Connection object or None
  """
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except Error as e:
    print(e)

  return conn

def createConfiguration(conn, newConfig):
  cur = conn.cursor()
  cur.execute('SELECT * FROM configs where name="{}"'.format(newConfig[0]))
  rows = cur.fetchall()
  if len(rows) == 0:
    sql = ''' INSERT INTO configs(name,json)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, newConfig)
    return cur.lastrowid
  else:
    return rows[0][0]

def createServer(conn, configId, server):
  # 1. Create record in the servers table:
  sql = ''' INSERT INTO servers(name,endpoint_url,timeout,active,security_mode,tag,json,nsm)
            VALUES(?,?,?,?,?,?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, server)
  # conn.commit()
  serverId = cur.lastrowid

  # 2. Add server into configuration:
  sql = ''' INSERT INTO config_servers(config_id,server_id)
            VALUES(?,?) '''
  cur = conn.cursor()
  configRecord=(configId,serverId)
  cur.execute(sql, configRecord)

  return serverId

def createVariable(conn, loggingVariable):
  sql = ''' INSERT INTO loggingNodes(server_id,display_name,opc_node_id,node_id,sampling_interval,publishing_interval,queue_size,discard_oldest,data_change_trigger,deadband_type,deadband_value,eu_range,active,historizing,readfrom,readtype,agentid,routeid,targetid,group_id,topic,tag,partition,json,store_expanded_values)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, loggingVariable)
  
  return cur.lastrowid

def main():

  global destinationDatabase
  global sourceDatabase
  global recreateDb
  global serverHostName
  global serverIpAddress
  global serverPortNumber
  global securityMode
  global numberOfServers
  global numberOfVariables
  global samplingInterval
  global publishingInterval
  global collectorConfigurationName
  global serverOptionsFileName


  totalservers = 0
  totalVariables = 0

  queueSize = round(publishingInterval / samplingInterval + 2)
	
  # Read advanced OPC UA server connection options from file.
  # To make sure that the OVL can resolve host name of the server to IP Address, define serverHostName (as returned in the GetEndpoints call), and serverIpAddress above
  

  if destinationDatabase == None or len(destinationDatabase) < 1:
    print("Error: destination file name is not defined, exiting.")
    return

  if recreateDb and sourceDatabase == None or len(sourceDatabase) < 1:
    print("Error: source database file name is not defined, exiting.")
    return

  if recreateDb and sourceDatabase != destinationDatabase:
    if not os.path.exists(sourceDatabase):
      print("Error: source database file does not exist, exiting.")
      return
    if os.path.exists(destinationDatabase):
      os.remove(destinationDatabase)
    shutil.copyfile(sourceDatabase, destinationDatabase)

  serverOptions = getServerJsonOptions(serverOptionsFileName, serverHostName, serverIpAddress)
  
  # create a database connection
  print("Opening database file at {}".format(destinationDatabase));
  conn = createConnection(destinationDatabase)
  with conn:
    index = 0
    configRecord = (
      collectorConfigurationName,
      ''
      )

    collectorConfigurationId = createConfiguration(conn, configRecord);

    while index < numberOfServers:
      index = index + 1
        # create a new project

      server = ('Server{:03d}'.format(index),
                'opc.tcp://{}:{}'.format(serverIpAddress, serverPortNumber),
                1000,
                1,
                securityMode,
                'Edmonton',
                serverOptions,
                ''
                )

      serverId = createServer(conn, collectorConfigurationId, server)
      totalservers = totalservers + 1
      variableIndex=0
      
      while variableIndex < numberOfVariables:
        loggingVariable = (
          serverId,
          'Variable{:04d}'.format(variableIndex),
          'ns=2;s=Demo.Massfolder_Dynamic.Variable{:04d}'.format(variableIndex),
          0,
          samplingInterval,
          publishingInterval,
          queueSize,
          1,
          0,
          0,
          0.0,
          0.0,
          1,  # Active
          0,0,0,0,0,0,
          1,
          '', # Topic
          '', # Tag
          0,
          '',
          1
          )
        createVariable(conn, loggingVariable)
        variableIndex = variableIndex + 1
        totalVariables = totalVariables + 1

      serverPortNumber = serverPortNumber + 1

  conn.commit()

  print("Created {} server records and {} logged variable records\n".format(totalservers, totalVariables))
  
if __name__ == '__main__':
  main()