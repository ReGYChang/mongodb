from utils import *
import os
import json

settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
output_path = settings_json["output_path"]

diff_time = 65 * 60
diff_time_check = 70 * 60
backup_end_time = int(read_process("date +%s"))
backup_start_time = backup_end_time - diff_time
keep_backup_time = read_process("date -d '-1 days' '+%Y%m%d%H'").strip()

primary = getPrimaryNode(port)
output_file = "{}/oplog/{}_mongodb_oplog".format(output_path,getCurrentHour())

mongodump2 = "mongodump \
    --host {} \
    -u {} \
    -p {} \
    --port {} \
    --authenticationDatabase=admin \
    --gzip \
    -d local \
    -c oplog.rs  \
    --query '{ts:{$gte:Timestamp({},1),$lte:Timestamp({},9999)}}' \
    -o {}/oplog/{}_mongodb_oplog".format(getPrimaryNode(port),username,password,port,backup_start_time,backup_end_time,output_path,getCurrentHour())

# ensure oplog dir exist
if (os.path.isdir(output_path + "/oplog") == False):
    read_process("mkdir -p {}/oplog".format(output_path))

# backup mongodb
mongodump(primary,username,password,port,output_file,True,True,backup_start_time,backup_end_time)

# ensure backup process within 5 mins (default)
if (int(read_process("date +%s")) - diff_time_check > backup_start_time):
    print("Fatal Error: oplog export time exceeded legal diff_time scope.Could not guarantee the data consistency.Should increase diff_time arg and adjust backup frequency.")

# check oplog file after backup process
if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(output_path,getCurrentHour())) == False):
    print("Fatal Error: oplog file does not exist, please checkout.")

# remove oplog file 1 day ago
if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(output_path,keep_backup_time))):
    os.remove("{}/oplog/{}_mongodb_oplog".format(output_path,keep_backup_time))
    print("Message: Remove oplog file one day ago.")
else:
    print("Message: There is no oplog file to remove.")
