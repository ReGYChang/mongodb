from utils import *
import os
import json

# import configuration
settings = open('/opt/OmniMongoDB/backup/settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
backup_path = settings_json["backup_path"]
isGzip = settings_json["is_gzip"]

# incremental backup configuration
diff_time = 65 * 60
diff_time_check = 70 * 60
backup_end_time = int(read_process("date +%s"))
backup_start_time = backup_end_time - diff_time
keep_backup_time = read_process("date -d '-1 days' '+%Y%m%d%H'").strip()

primary = getPrimaryNode(port)
output_file = "{}/oplog/{}_mongodb_oplog".format(backup_path,getCurrentHour())

# ensure oplog dir exist
if (os.path.isdir(backup_path + "/oplog") == False):
    read_process("mkdir -p {}/oplog".format(backup_path))

# backup mongodb oplog
mongodump(primary,username,password,port,output_file,isGzip,True,backup_start_time,backup_end_time)

# ensure backup process within 5 mins (default)
if (int(read_process("date +%s")) - diff_time_check > backup_start_time):
    printlog("Fatal Error: Oplog export time exceeded legal diff_time scope.Could not guarantee the data consistency.Should increase diff_time arg and adjust backup frequency.")
else:
    printlog("Message: Backup oplog process check completed successfully.")

# check oplog file after backup process
if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(backup_path,getCurrentHour())) == False):
    printlog("Fatal Error: Oplog file does not exist, please checkout.")
else:
    printlog("Message: Oplog file check completed successfully.")

# remove oplog file 1 day ago
if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(backup_path,keep_backup_time))):
    os.remove("{}/oplog/{}_mongodb_oplog".format(backup_path,keep_backup_time))
    printlog("Message: Remove oplog file one day ago.")
else:
    printlog("Message: There is no oplog file to remove.")
