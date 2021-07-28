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
backup_end_time = read_process("date +%s")
backup_start_time = backup_end_time - diff_time

mongodump = "mongodump \
    --host {} \
    -u {} \
    -p {} \
    --authenticationDatabase=admin \
    --port {} \
    --gzip \
    -d local \
    -c oplog.rs  \
    --query '{ts:{$gte:Timestamp({},1),$lte:Timestamp({},9999)}}' \
    -o /opt/OmniMongoDB/backup/oplog/{}_mongodb_oplog".format(getPrimaryNode(port),username,password,port,backup_start_time,backup_end_time,getCurrentHour())

if (os.path.isdir(output_path + "/oplog") == False):
    read_process("mkdir -p {}/oplog".format(output_path))

read_process("{}".format(mongodump))

