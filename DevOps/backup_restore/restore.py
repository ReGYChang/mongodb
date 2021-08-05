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

# Unix epoch, default is "0"
oplog_limit = 0
# hours, default is "0"
restore_timelimit = 1

current_time = getCurrentHour().strip()
restore_target_time = read_process("date -d '-{} hours' '+%Y%m%d%H'".format(restore_timelimit)).strip()

primary = getPrimaryNode(port)
oplog_files = os.listdir("/opt/OmniMongoDB/backup/oplog")
full_backup_files = os.listdir("/opt/OmniMongoDB/backup")

if os.path.isdir("/tmp/emptyDirForOpRestore") == False:
    read_process("mkdir -p /tmp/emptyDirForOpRestore")

# ensure full backup file exists
if os.path.isdir("{}/{}_mongodb_backup".format(backup_path,restore_target_time[:7])) == False:
    print("Fatal Error: Full backup dir does not exist, please checkout.")
    exit()
else:
    print("Message: Full backup dir check completed successfully.")

# ensure oplog file exists
if os.path.isdir("{}/oplog".format(backup_path)) == False:
    print("Fatal Error: Oplog dir does not exist, please checkout.")
    exit()
else:
    print("Message: Oplog dir check completed successfully.")

print("Message: Start to process full data recovery.")

mongorestore(primary,username,password,port,"{}/{}_mongodb_backup".format(backup_path,restore_target_time[:7]),isGzip,False)

print("Message: Start to process incremental recovery up to date.")

for oplog in oplog_files:
    oplog_time = re.findall(r"\d+",oplog)[0]
    if oplog_time[:7] == restore_target_time[:7] and int(oplog_time) <= int(current_time):
        print("Message: Applying oplog {}.".format(oplog_time))
        oplog_file = "{}/oplog/{}/local/oplog.rs.bson".format(backup_path,oplog)
        mongorestore(primary,username,password,port,oplog_file,isGzip,True,oplog_limit)