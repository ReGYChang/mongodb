from utils import *
import os
import json

# import configuration
settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
backup_path = settings_json["backup_path"]
isGzip = settings_json["is_gzip"]

# default is "0"
restore_timelimit = 1

# default is "0"
oplog_limit = 0

primary = getPrimaryNode(port)
today = getCurrentDate()
restore_target_time = int(read_process("date +%s")) - restore_timelimit * 60
oplog_files = os.listdir("/opt/OmniMongoDB/backup/oplog")

# ensure oplog file exists
if(os.path.isdir("{}/oplog") == False):
    print("Fatal Error: Oplog dir does not exist, please checkout.")
else:
    print("Message: Oplog dir check completed successfully.")


if restore_timelimit == 0:
    print("Message: Start to process full data recovery.")
    mongorestore(primary,username,password,port,"{}/{}_mongodb_backup".format(backup_path,today),isGzip,False)
else:
    print("Message: Start to process full data recovery.")
    mongorestore(primary,username,password,port,"{}/{}_mongodb_backup".format(backup_path,today),isGzip,False)

    print("Message: Start to process point-in-time recovery.")
    for oplog in oplog_files:
        oplog_time = re.findall(r"\d+")[0]
        if oplog_time[:5] == today and int(oplog_time) < (int(getCurrentHour()) - restore_timelimit):
            print("Message: Applying oplog {}.".format(oplog_time))
            oplog_file = "{}/oplog/{}/local/oplog.rs.bson".format(backup_path,oplog)
            mongorestore(primary,username,password,port,oplog_file,isGzip,True,oplog_limit)