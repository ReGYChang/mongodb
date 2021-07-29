from utils import *
import json

# import configuration
settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
output_path = settings_json["output_path"]

secondary = getSecondaryNode(port)
output_file = "{}/{}_mongodb_backup".format(output_path,getCurrentDate())

# fsyncLock secondary node
mongosh(secondary,username,password,port,"db.fsyncLock();")

# full backup mongodb data
mongodump(secondary,username,password,port,output_file,True,False)

# fsyncUnlock secondary node
mongosh(secondary,username,password,port,"db.fsyncUnlock();")