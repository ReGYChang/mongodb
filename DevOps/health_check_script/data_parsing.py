import json
import re
from utils import *

read_process("touch linux.json")

path = 'mongodb-ubuntu-1_health_check_2021-09-22/cpu-info.txt'
f = open(path,'r')
cpu_info = f.read()
cpu_cores = re.findall(r"^CPU\(s\).+\d",cpu_info,re.M)[0].split(":")[1].strip()
cpu_model = re.findall(r"^Model name:.+",cpu_info,re.M)[0].split(":")[1].strip()
hypervisor = re.findall(r"^Hypervisor.+",cpu_info,re.M)
f.close()

path = 'os-version.txt'
f = open(path,'r')
os_version = f.read().strip()
f.close

path = 'mem-info.txt'
f = open(path,'r')
mem_info = f.read().strip()
mem_space = re.findall(r"^Mem.+",mem_info)[0].split()[1]
swap_space = re.findall(r"^Swap.+",mem_info)[0].split()[1]
mem_swap = mem_space + '/' + swap_space
f.close

path = 'disk-info.txt'
f = open(path,'r')
disk_info = f.read().strip()
home_space_total = re.findall(r".+\/$",disk_info)[1].split()[1]
home_space_used = re.findall(r".+\/$",disk_info)[1].split()[2]
f.close

path = 'uptime.txt'
f = open(path,'r')
uptime = f.read().strip(',')[0]
f.close

path = 'ulimit.txt'
f = open(path,'r')
ulimit = f.read().strip()
ulimit_nproc = re.findall(r"^Max processes.+",ulimit,re.M)[0].split()[2]
ulimit_nofile = re.findall(r"^Max open files.+",ulimit,re.M)[0].split()[2]
f.close

# path = 'readahead.txt'
# f = open(path,'r')
# ulimit = f.read().strip()
# readahead = re.findall(r"^Max processes.+",ulimit,re.M)[0].split()[2]
# f.close

path = 'thp_enabled.txt'
f = open(path,'r')
thp_enabled = f.read().strip()
if len(re.findall(r"\[never\]")) > 0:
    thp_enabled_flag = True
else:
    thp_enabled_flag = False
f.close

path = 'thp_defrag.txt'
f = open(path,'r')
thp_enabled = f.read().strip()
if len(re.findall(r"\[never\]")) > 0:
    thp_defrag_flag = True
else:
    thp_defrag_flag = False
f.close

path = 'thp_defrag.txt'
f = open(path,'r')
thp_enabled = f.read().strip()
if len(re.findall(r"\[never\]")) > 0:
    thp_defrag_flag = True
else:
    thp_defrag_flag = False
f.close

path = 'vm_zone_reclaim_mode.txt'
f = open(path,'r')
vm_zone_reclaim_mode = f.read().strip()
f.close

path = 'vm_swappiness.txt'
f = open(path,'r')
vm_swappiness = f.read().strip()
f.close