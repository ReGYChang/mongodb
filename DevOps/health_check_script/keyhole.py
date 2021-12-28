import os
import json
from utils import *
from subprocess import check_output

def runcmd(command):
    ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
    if ret.returncode == 0:
        print("success:",ret)
    else:
        print("error:",ret)

config_data = open('config.json')
config_json = json.load(config_data)
mongo_hosts = config_json["hosts"]

for host in mongo_hosts:

    config_path = host["mongod_conf"]
    mongod_name = host["mongod_name"]
    username = host["username"]
    password = host["password"]

    # read mongod.conf
    with open("{}".format(config_path),"r") as config_data:
        try:
            mongod_conf = config_data.read()
        except Exception as e:
            print(e)

    mongodb_port = re.findall(r"(port.+)",mongod_conf)[0].split(':')[1].strip()
    mongodb_dbpath = re.findall(r"(dbPath.+)",mongod_conf)[0].split(':')[1].strip()
    log_path = re.findall(r"(path.+)",mongod_conf)[0].split(':')[1].strip()


read_process("./keyhole_amd -allinfo mongodb://{}:{}@localhost:{}".format(username,password,mongodb_port))
read_process("./keyhole_amd -loginfo {}".format(log_path))

runcmd("./keyhole_amd -allinfo mongodb://{}:{}@localhost:{}".format(username,password,mongodb_port))
runcmd("./keyhole_amd -loginfo {}".format(log_path))