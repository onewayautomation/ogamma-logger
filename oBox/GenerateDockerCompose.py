#!/usr/bin/python

import sys

def parse_file(file_path):
    # Create an empty set to store key-value pairs
    key_value_set = set()

    # Open the file
    with open(file_path, 'r', encoding = "utf-8") as file:
        # Read lines one by one
        for line in file:
            if line.startswith('#'):
                continue
            if line.endswith('\n'):
              line = line[:-1]
            
            try:
              # Strip whitespace and split the line into key-value pair
              key, value = line.strip().split('=')
              # Add the key-value pair to the set
              key_value_set.add((key, value))
            except:
              continue

    return key_value_set
    
def main(argv):
  inputfile = './docker-compose-template.yml'
  outputfile = './docker-compose.yml'
  envFileName = "./.env"
  t = ""
  with open(inputfile, "r", encoding = "utf-8") as reader:
    try:
      t = reader.read()
    except:
      print("Failed to read file {}".format(inputfile))
      sys.exit(2)
  try:
    envVars = parse_file(envFileName)
  except:
    print("Failed to read file with environment variables " + envFileName)
    sys.exit(2)   
    
  hostName = ""
  for key, value in envVars:
    t = t.replace("${"+key+"}", value)
    if key == "REVERSE_PROXY_HOST":
      hostName = value

  with open(outputfile, "w", encoding = "utf-8") as writer:
    writer.write(t)

  # Set host name in the Grafana ini file:
  if hostName != "":
    t = ""
    grafanaInputFile = "./grafana/grafana-template.ini"
    grafanaOutputFile = "./grafana/grafana.ini"

    with open(grafanaInputFile, "r", encoding = "utf-8") as reader:
      t = reader.read()
    t = t.replace("#domain = localhost", "domain = "+hostName)
    t = t.replace("# root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana", "root_url = https://" + hostName + "/grafana/")
    with open(grafanaOutputFile, "w", encoding = "utf-8") as writer:
      writer.write(t)

if __name__ == "__main__":
  main(sys.argv[1:])