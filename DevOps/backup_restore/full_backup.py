from utils import *
import json

# import configuration
settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
output_path = settings_json["output_path"]
output_file = "{}/{}_mongodb_backup".format(output_path,getCurrentDate())
secondary = getSecondaryNode(port)
keep_backup_time = read_process("date -d '-7 days' '+%Y%m%d'").strip()

# fsyncLock secondary node
mongosh(secondary,username,password,port,"db.fsyncLock();")

# full backup mongodb data
mongodump(secondary,username,password,port,output_file,True,False)

# fsyncUnlock secondary node
mongosh(secondary,username,password,port,"db.fsyncUnlock();")

# check full backup file after backup process
if(os.path.isdir(output_file) == False):
    print("Fatal Error: Full backup file does not exist, please checkout.")
else:
    print("Message: Full backup file check completed successfully.")

# remove full backup file 1 day ago
if(os.path.isdir("{}/{}_mongodb_backup".format(output_path,keep_backup_time))):
    os.remove("{}/{}_mongodb_backup".format(output_path,keep_backup_time))
    print("Message: Remove full backup file one day ago.")
else:
    print("Message: There is no full backup file to remove.")