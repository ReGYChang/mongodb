import json
import re
from utils import *

read_process("touch linux.json")

# import mongodb configuration
config_data = open('config.json')
config_json = json.load(config_data)
mongo_hosts = config_json["hosts"]
mongod_name = "rs0_0"

today = date.today()
hostname = read_process("hostname").strip()
output_dir = "{}_health_check_{}".format(hostname,today)
output_path = "./{}".format(output_dir)

path = '{}/cpu-info.txt'.format(output_path)
f = open(path,'r')
cpu_info = f.read()
cpu_cores = re.findall(r"^CPU\(s\).+\d",cpu_info,re.M)[0].split(":")[1].strip()
cpu_model = re.findall(r"^Model name:.+",cpu_info,re.M)[0].split(":")[1].strip()
hypervisor = re.findall(r"^Hypervisor.+",cpu_info,re.M)
f.close()

path = '{}/os-version.txt'.format(output_path)
f = open(path,'r')
os_version = f.read().strip()
f.close

path = '{}/mem-info.txt'.format(output_path)
f = open(path,'r')
mem_info = f.read().strip()
mem_space = re.findall(r"^Mem.+",mem_info)[0].split()[1]
swap_space = re.findall(r"^Swap.+",mem_info)[0].split()[1]
mem_swap = mem_space + '/' + swap_space
f.close

path = '{}/disk-info.txt'.format(output_path)
f = open(path,'r')
disk_info = f.read().strip()
home_space_total = re.findall(r".+\/$",disk_info)[1].split()[1]
home_space_used = re.findall(r".+\/$",disk_info)[1].split()[2]
f.close

path = '{}/uptime.txt'.format(output_path)
f = open(path,'r')
uptime = f.read().strip(',')[0]
f.close

path = '{}/ulimit.txt'.format(output_path)
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

path = '{}/thp_enabled.txt'.format(output_path)
f = open(path,'r')
thp_enabled = f.read().strip()
if len(re.findall(r"\[never\]",thp_enabled)) > 0:
    thp_enabled_flag = True
else:
    thp_enabled_flag = False
f.close

path = '{}/thp_defrag.txt'.format(output_path)
f = open(path,'r')
thp_defrag = f.read().strip()
if len(re.findall(r"\[never\]",thp_defrag)) > 0:
    thp_defrag_flag = True
else:
    thp_defrag_flag = False
f.close

path = '{}/vm_zone_reclaim_mode.txt'.format(output_path)
f = open(path,'r')
vm_zone_reclaim_mode = f.read().strip()
f.close

path = '{}/vm_swappiness.txt'.format(output_path)
f = open(path,'r')
vm_swappiness = f.read().strip()
f.close

path = '{}/mongodb_version.txt'.format(output_path)
f = open(path,'r')
mongodb_version = f.read().strip()
f.close

path = '{}/{}/mongodb_fcv.txt'.format(output_path,mongod_name)
f = open(path,'r')
mongodb_fcv = f.read().strip()
mongodb_fcv = re.findall(r"version.+",mongodb_fcv)[0].split(":").strip("\"")
f.close

path = '{}/mongodb_port.txt'.format(output_path)
f = open(path,'r')
mongodb_port = f.read().strip()
f.close

path = '{}/uptime.txt'.format(output_path)
f = open(path,'r')
uptime = f.read().strip()
uptime = uptime.split(",")[0]
f.close

path = '{}/{}mongodb_serverStatus.txt'.format(output_path,mongod_name)
f = open(path,'r')
mongodb_serverStatus = f.read().strip()
serverStatus_uptime = re.findall(r"\"uptime\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_asserts_warning = re.findall(r"\"warning\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_asserts_user = re.findall(r"\"user\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_connections = re.findall(r"\"connections\".+(\n.+){4}",mongodb_serverStatus)[0].split(":")[1]
serverStatus_connections_current = re.findall(r"\"current\".+",serverStatus_connections)[0].split(":")[1]
serverStatus_connections_available = re.findall(r"\"available\".+",serverStatus_connections)[0].split(":")[1]
serverStatus_extra_info_page_faults = re.findall(r"\"page_fault\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_opLatencies_reads = re.findall(r"\"reads\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1]
serverStatus_opLatencies_writes = re.findall(r"\"writes\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1]
serverStatus_opLatencies_reads_latency = re.findall(r"\"latency\".+",serverStatus_opLatencies_reads)[0].split(":")[1]
serverStatus_opLatencies_reads_ops = re.findall(r"\"ops\".+",serverStatus_opLatencies_reads)[0].split(":")[1]
serverStatus_opLatencies_writes_latency = re.findall(r"\"latency\".+",serverStatus_opLatencies_writes)[0].split(":")[1]
serverStatus_opLatencies_writes_ops = re.findall(r"\"ops\".+",serverStatus_opLatencies_writes)[0].split(":")[1]
serverStatus_cursor_timedOut = re.findall(r"\"timedOut\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_operation_scanAndOrder = re.findall(r"\"scanAndOrder\".+",mongodb_serverStatus)[0].split(":")[1]
serverStatus_operation_writeConflicts = re.findall(r"\"writeConflicts\".+",mongodb_serverStatus)[0].split(":")[1]
f.close




