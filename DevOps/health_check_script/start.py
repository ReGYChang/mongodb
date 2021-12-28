import os
import json
from utils import *

path = './'

for f in os.listdir(path):
    if f.endswith('txt'):
        print(f)
        os.rename(f, os.path.splitext(f)[0] +'.js')

output_healthCheck = read_process("python ./health_check_repl.py")
