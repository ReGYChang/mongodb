from utils import *
import json

settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
output_path = settings_json["output_path"]

mongodump = "mongodump \
    --host {} \
    -u {} \
    -p {} \
    --authenticationDatabase=admin \
    --port {} \
    --gzip \
    -o /opt/OmniMongoDB/backup/{}_mongodb_backup".format(getSecondaryNode(port),username,password,port,getCurrentDate())

mongosh = "mongo \
    --host {} \
    -u {} \
    -p {} \
    --authenticationDatabase=admin  \
    --port {} \
    --eval ".format(getSecondaryNode(port),username,password,port)

read_process("{} {}".format(mongosh,"'db.fsyncLock();'"))

read_process("{}".format(mongodump))

read_process("{} {}".format(mongosh,"'db.fsyncUnlock();'"))