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
