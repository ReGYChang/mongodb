import json
import re
from utils import *

read_process("touch linux.json")

path = 'mongodb-ubuntu-1_health_check_2021-09-22/cpu-info.txt'
f = open(path,'r')
cpu_info = f.read()
f.close()

cpu_cores = re.findall(r"^CPU\(s\).+\d",cpu_info,re.M)[0].split(":")[1].strip()
cpu_model = re.findall(r"^Model name:.+",cpu_info,re.M)[0].split(":")[1].strip()


print(cpu_cores)
print(cpu_model)
