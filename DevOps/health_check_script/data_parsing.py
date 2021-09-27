import json
import re
from utils import *

read_process("touch linux.json")

path = 'cpu-info.txt'
f = open(path,'r')
print(f.read())
cpu_info = f.read()
f.close()

cpu_cores = re.search("^(CPU\(s\)).+\d",cpu_info)
cpu_model = re.search("^Model name:.+",cpu_info)