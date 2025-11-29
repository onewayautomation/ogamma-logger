# This project is built using materials from https://www.sqlitetutorial.net/sqlite-python/

from optparse import Option
import sqlite3
from sqlite3 import Error

# To install module psycopg2, run command:  pip3 install psycopg2

import psycopg2

import json
import os
import shutil
import math
import sys

# Before running of the script, set test options below as required.
# These options can be set also in json file, if its name is passed as command line argument. See file options.json as example.

collectorConfigurationName = 'Test Configuration'
 
# Alternative:
# AdatabaseType="PostgreSQL"
# ApsqlDatabaseName = "ogammaloggerconfig"
# ApsqlUserName = "ogamma"
# ApsqlPassword = "ogamma"
# ApsqlHost = "localhost"
# psqlPort=5432

databaseType="SQLite"

# Name of the SQLite database file where configuration is created. Required option.
# Can be existing file. If existing file, and recrteadeDb is true, then will be overritten by the souirce file. If recreateDb is false, then will be used as is.
# Note that if this file is configured to be used by OVL, then the OVL process must be stopped before and running this script.

sqliteDatabaseName = '../data/config.db'
# destinationDatabase = '../docker/data/config.db'

# template database, which can be used as a base SQLite database file. Optional.
sourceDatabase = './config-template.db'

# If true, and source database fiel exists, then destination file is overwrittem with copy of the source file.
# This is expected to be the case when this script runs multiple times, to prevent addning more records additionally to existing records.
recreateDb = False

# Hostname of the machine where OPC UA Server runs.
serverHostName = 'owas'

# Ip address of the machine where OPC UA Server runs. This is used to resolve host name to IP address.
serverIpAddress = '192.168.1.79'

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
numberOfServers = 50
		
# Logged variables per server
numberOfVariables = 100
samplingInterval=1000
publishingInterval=1000

variablesPerPartition=10

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

def createConnection():
  global databaseType
  global sqliteDatabaseName
  global psqlDatabaseName
  global psqlUserName
  global psqlPassword
  global psqlHost 
  global psqlPort

  conn = None

  if databaseType == "SQLite":
    # create a database connection to the SQLite database specified by global variable sqliteDatabaseName
    try:
      conn = sqlite3.connect(sqliteDatabaseName)
    except Error as e:
      print(e)
  elif databaseType == "PostgreSQL":
    try:
      conn = psycopg2.connect(database=psqlDatabaseName, user=psqlUserName, password=psqlPassword, host=psqlHost, port=psqlPort)
    except Error as e: 
      print(e)
  else:
    print("Invalid database type!\n")

  return conn

def createConfiguration(conn, newConfig):
  cur = conn.cursor()
  cur.execute("SELECT * FROM configs where name='{}'".format(newConfig[0]))
  rows = cur.fetchall()
  if len(rows) == 0:
    sql = "INSERT INTO configs(name,json) VALUES('{}','')".format(newConfig[0])
    cur = conn.cursor()
    cur.execute(sql)

    cur = conn.cursor()
    cur.execute("SELECT * FROM configs where name='{}'".format(newConfig[0]))
    rows = cur.fetchall()
    return rows[0][0]
  else:
    return rows[0][0]

def createServer(conn, configId, server):
  # 1. Create record in the servers table:
  if databaseType=="SQLite":
    sql = "INSERT INTO servers(name,endpoint_url,timeout,active,security_mode,tag,json,nsm) VALUES(?,?,?,?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, server)
    serverId = cur.lastrowid
  else:
    sql = "INSERT INTO servers(name,endpoint_url,timeout,active,security_mode,tag,json,nsm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) returning id"
    cur = conn.cursor()
    cur.execute(sql, server)
    serverId = cur.fetchone()[0]

  # 2. Add server into configuration:
  sql = "INSERT INTO config_servers(config_id,server_id) VALUES({},{})".format(configId, serverId)
  cur = conn.cursor()
  cur.execute(sql)
  

  return serverId

def createVariable(conn, loggingVariable):
  if databaseType=="SQLite":
    sql = ''' INSERT INTO loggingNodes (server_id,display_name,opc_node_id,node_id,sampling_interval,publishing_interval,queue_size,discard_oldest,data_change_trigger,deadband_type,deadband_value,eu_range,active,historizing,readfrom,readtype,agentid,routeid,targetid,group_id,topic,tag,partition,json,store_expanded_values)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''' 
  else:
    sql = ''' INSERT INTO public."loggingNodes" (server_id,display_name,opc_node_id,node_id,sampling_interval,publishing_interval,queue_size,discard_oldest,data_change_trigger,deadband_type,deadband_value,eu_range,active,historizing,readfrom,readtype,agentid,routeid,targetid,group_id,topic,tag,partition,json,store_expanded_values)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
  cur = conn.cursor()
  cur.execute(sql, loggingVariable)
  
  return cur.lastrowid

def main(args):
  global collectorConfigurationName

  global databaseType
  global sqliteDatabaseName
  global sourceDatabase
  global recreateDb

  global psqlDatabaseName
  global psqlUserName
  global psqlPassword
  global psqlHost
  global psqlPort

  global numberOfServers
  global serverHostName
  global serverIpAddress
  global serverPortNumber
  global securityMode
  global serverOptionsFileName

  global numberOfVariables
  global variablesPerPartition
  global samplingInterval
  global publishingInterval

  if len(args) > 1:
    # Read options from json config file:
    fileName = args[1]
    print("Reading options from configuration file {}".format(fileName))
    f = open(fileName, "r")
    content = f.read()
    f.close()

    options = json.loads(content)

    if "collectorConfigurationName" in options:
      collectorConfigurationName = options["collectorConfigurationName"]

    if "databaseType" in options:
      databaseType = options["databaseType"]

    if databaseType=="PostgreSQL":
      if "psqlDatabaseName" in options:
        psqlDatabaseName = options["psqlDatabaseName"]
      if "psqlUserName" in options:
        psqlUserName = options["psqlUserName"]
      if "psqlPassword" in options:
        psqlPassword = options["psqlPassword"]
      if "psqlHost" in options:
        psqlHost = options["psqlHost"]
      if "psqlPort" in options:
        psqlPort = options["psqlPort"]

    elif databaseType=="SQLite":
      sqliteDatabaseName = options["sqliteDatabaseName"]
      if "sourceDatabase" in options: 
        sourceDatabase = options["sourceDatabase"]
      if "recreateDb" in options:
        recreateDb = options["recreateDb"]

    if "serverHostName" in options:
      serverHostName = options["serverHostName"]
    if "serverIpAddress" in options:
      serverIpAddress = options["serverIpAddress"]
    if "serverPortNumber" in options:
      serverPortNumber = options["serverPortNumber"]
    if "securityMode" in  options:
      securityMode = options["securityMode"]
    if "numberOfServers" in options:
      numberOfServers = options["numberOfServers"]
    if "serverOptionsFileName" in options:
      serverOptionsFileName = options["serverOptionsFileName"]

    if "numberOfVariables" in options:
      numberOfVariables = options["numberOfVariables"]
    if "variablesPerPartition" in options:
      variablesPerPartition = options["variablesPerPartition"]
    if "samplingInterval" in options:
      samplingInterval = options["samplingInterval"]
    if publishingInterval in options:
      publishingInterval = options["publishingInterval"]

  totalservers = 0
  totalVariables = 0

  queueSize = round(publishingInterval / samplingInterval) + 2
	
  # Read advanced OPC UA server connection options from file.
  # To make sure that the OVL can resolve host name of the server to IP Address, define serverHostName (as returned in the GetEndpoints call), and serverIpAddress above
  
  if databaseType=="SQLite":
    isActive = 1
    discardOldest=1
    isHistorizing=0
    if sqliteDatabaseName == None or len(sqliteDatabaseName) < 1:
      print("Error: destination file name is not defined, exiting.")
      return

    if recreateDb and sourceDatabase == None or len(sourceDatabase) < 1:
      print("Error: source database file name is not defined, exiting.")
      return

    if recreateDb and sourceDatabase != sqliteDatabaseName:
      if not os.path.exists(sourceDatabase):
        print("Error: source database file does not exist, exiting.")
        return
      if os.path.exists(sqliteDatabaseName):
        os.remove(sqliteDatabaseName)
      shutil.copyfile(sourceDatabase, sqliteDatabaseName)
  else:
    isActive=True
    discardOldest=True
    isHistorizing=False
  serverOptions = getServerJsonOptions(serverOptionsFileName, serverHostName, serverIpAddress)
  
  # create a database connection
  if databaseType=="SQLite":
    print("Opening database file at {}".format(sqliteDatabaseName))
  else:
    print("Connecting to the database {} at server {}:{}", psqlDatabaseName, psqlHost, psqlPort)
  conn = createConnection()
  with conn:
    index = 0
    configRecord = (
      collectorConfigurationName,
      ''
      )

    collectorConfigurationId = createConfiguration(conn, configRecord);
    allVariablesIndex = 0
    while index < numberOfServers:
      index = index + 1
        # create a new project

      server = ('Server{:03d}'.format(index),
                'opc.tcp://{}:{}'.format(serverIpAddress, serverPortNumber),
                1000,
                isActive,
                securityMode,
                'Server{}'.format(index),   # Tag
                serverOptions,              # advanced options - json string
                ''
                )

      serverId = createServer(conn, collectorConfigurationId, server)
      totalservers = totalservers + 1
      variableIndex=0
      
      while variableIndex < numberOfVariables:
        # Partition number if in scope of each server:
        if variablesPerPartition <= 1:
          partitionNumber = 0
        else:
          partitionNumber = math.floor(variableIndex / variablesPerPartition)

        # Alternative way to define partition number: in scope of all variables:
        #partitionNumber = math.floor(allVariablesIndex / variablesPerPartition)
        
        allVariablesIndex = allVariablesIndex+1
        
        loggingVariable = (
          serverId,                                                               # serverId
          'Variable{:04d}'.format(variableIndex),                                 # display_name
          'ns=2;s=Demo.Massfolder_Dynamic.Variable{:04d}'.format(variableIndex),  # opc_node_id
          0,                                                                      # node_id
          samplingInterval,   # sampling_interval
          publishingInterval, # publishing_interval
          queueSize,          # queue_size
          discardOldest,      # discard_oldest
          0,                  # data_change_trigger
          0,                  # deadband_type
          0.0,                # deadband_value
          0.0,                # eu_range
          isActive,           # active
          isHistorizing,      # historizing
          0,                  # readfrom
          0,                  # readtype
          0,                  # agentid
          0,                  # routeId
          0,                  # targetid
          1,                  # group_id
          '',                 # Topic 
          '',                 # Tag
          partitionNumber,    # partition
          '',                 # json
          1                   # store_expanded_values
          )
        createVariable(conn, loggingVariable)
        variableIndex = variableIndex + 1
        totalVariables = totalVariables + 1

      serverPortNumber = serverPortNumber + 1

  conn.commit()

  print("Created {} server records and {} logged variable records\n".format(totalservers, totalVariables))

if __name__ == "__main__":
  args = sys.argv
  main(args)