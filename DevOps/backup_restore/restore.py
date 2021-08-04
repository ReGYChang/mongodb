from utils import *
import os
import json

# import configuration
settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
backup_path = settings_json["output_path"]

# default is "0"
restore_timelimit = 1
primary = getPrimaryNode(port)
restore_target_time = int(read_process("date +%s")) - restore_timelimit * 60

# ensure oplog file exists
if(os.path.isdir("{}/oplog") == False):
    print("Fatal Error: Oplog dir does not exist, please checkout.")
else:
    print("Message: Oplog dir check completed successfully.")

oplog_files = os.listdir("/opt/OmniMongoDB/backup/oplog")

for oplog in oplog_files:
    oplog_time = re.findall(r"\d+")[0]
    if oplog_time[:5] == getCurrentDate() and int(oplog_time) < (int(getCurrentHour()) - restore_timelimit):
        print("Message: Applying oplog {}.".format(oplog_time))
        mongorestore(primary,username,password,port,)



if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(output_path,getCurrentHour() - restore_timelimit)) == False):
    print("Fatal Error: Oplog file does not exist, please checkout.")
else:
    print("Message: Oplog file check completed successfully.")
