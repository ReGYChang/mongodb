from utils import *
import os
import json

# import configuration
settings = open('settings.json')
settings_json = json.load(settings)

username = settings_json["username"]
password = settings_json["password"]
port = settings_json["port"]
output_path = settings_json["output_path"]

restore_timelimit = 1
restore_target_time = int(read_process("date +%s")) - restore_timelimit * 60

# ensure oplog file exists
if(os.path.isdir("{}/oplog/{}_mongodb_oplog".format(output_path,getCurrentHour() - restore_timelimit)) == False):
    print("Fatal Error: Oplog file does not exist, please checkout.")
else:
    print("Message: Oplog file check completed successfully.") 
