import json
import re
from utils import *
from datetime import date


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

path = '{}/cpu-info2.txt'.format(output_path)
f = open(path,'r')
cpu_info = f.read()
cpu_cores = re.findall(r"^CPU\(s\).+\d",cpu_info,re.M)[0].split(":")[1].strip()
cpu_model = re.findall(r"^Model name:.+",cpu_info,re.M)[0].split(":")[1].strip()
hypervisor = re.findall(r"^Hypervisor.+",cpu_info,re.M)[0].split(":")[1].strip()
print("cpu cores: " + cpu_cores)
print("cpu model: " + cpu_model)
print("hypervisor: " + hypervisor)
f.close()

path = '{}/os-version.txt'.format(output_path)
f = open(path,'r')
os_version = f.read().strip()
print("os version: " + os_version)
f.close

path = '{}/mem-info.txt'.format(output_path)
f = open(path,'r')
mem_info = f.read().strip()
mem_space = re.findall(r"^Mem.+",mem_info,re.M)[0].split()[1]
swap_space = re.findall(r"^Swap.+",mem_info,re.M)[0].split()[1]
mem_swap = mem_space + '/' + swap_space
print("mem swap space: " + mem_swap)
f.close

path = '{}/disk-info2.txt'.format(output_path)
f = open(path,'r')
disk_info = f.read().strip()
home_space_total = re.findall(r".+\/$",disk_info,re.M)[0].split()[1]
home_space_used = re.findall(r".+\/$",disk_info,re.M)[0].split()[2]
print("home space total: " + home_space_total)
print("home space used: " + home_space_used)
f.close

path = '{}/uptime.txt'.format(output_path)
f = open(path,'r')
uptime = f.read().strip('').split(",")[0]
print("uptime: " + uptime)
f.close

path = '{}/ulimit.txt'.format(output_path)
f = open(path,'r')
ulimit = f.read().strip()
ulimit_nproc = re.findall(r"^Max processes.+",ulimit,re.M)[0].split()[3]
ulimit_nofile = re.findall(r"^Max open files.+",ulimit,re.M)[0].split()[4]
print("ulimit nproc: " + ulimit_nproc)
print("ulimit nofile: " + ulimit_nofile)
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
print("vm zone reclaim mode: " + vm_zone_reclaim_mode)
f.close

path = '{}/vm_swappiness.txt'.format(output_path)
f = open(path,'r')
vm_swappiness = f.read().strip()
print("vm swappiness: " + vm_swappiness)
f.close

path = '{}/mongodb_version.txt'.format(output_path)
f = open(path,'r')
mongodb_version = f.read().strip()
mongodb_version = re.findall(r"v[\d.]+",mongodb_version)[0]
print("mongodb version: " + mongodb_version)
f.close

path = '{}/{}/mongodb_fcv.txt'.format(output_path,mongod_name)
f = open(path,'r')
mongodb_fcv = f.read().strip()
mongodb_fcv = re.findall(r"version.+",mongodb_fcv)[0].split(":")[1].strip().strip("\"")
print("mongodb fcv: " + mongodb_fcv)
f.close

path = '{}/mongodb_port.txt'.format(output_path)
f = open(path,'r')
mongodb_port = f.read().strip()
print("mongodb port: " + mongodb_port)
f.close

path = '{}/uptime.txt'.format(output_path)
f = open(path,'r')
uptime = f.read().strip()
uptime = uptime.split(",")[0]
print("uptime: " + uptime)
f.close

path = '{}/{}/mongodb_serverStatus.txt'.format(output_path,mongod_name)
f = open(path,'r')
mongodb_serverStatus = f.read().strip()

serverStatus_uptime = re.findall(r"\"uptime\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
print("Server status uptime: " + serverStatus_uptime)

serverStatus_asserts_warning = re.findall(r"\"warning\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')

serverStatus_asserts_user = re.findall(r"\"user\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
print("Server status asserts user: " + serverStatus_asserts_user)

# serverStatus_connections = re.findall(r"\"connections\".+(\n.+){4}",mongodb_serverStatus)[0].split(":")[1]
# print("Server status connections: " + serverStatus_connections)

serverStatus_connections_current = re.findall(r"\"connections\"(.+\n){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
print("Server status connections current: " + serverStatus_connections_current)

serverStatus_connections_available = re.findall(r"\"connections\"(.+\n){3}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
print("Server status connections available: " + serverStatus_connections_available)

serverStatus_extra_info_page_faults = re.findall(r"\"page_faults\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_extra_info_page_faults = re.findall(r"\d+",serverStatus_extra_info_page_faults)[0]
print("Server status extra info page faults: " + serverStatus_extra_info_page_faults)

# serverStatus_opLatencies_reads = re.findall(r"\"reads\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip()
# print("Server status oplatencies reads: " + serverStatus_opLatencies_reads)

# serverStatus_opLatencies_writes = re.findall(r"\"writes\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip()
# print("Server status oplatencies writes: " + serverStatus_opLatencies_writes)

serverStatus_opLatencies_reads_latency = re.findall(r"\"reads\".+(\n.+){1}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_opLatencies_reads_latency = re.findall(r"\d+",serverStatus_opLatencies_reads_latency)[0]
print("Server status oplatencies reads latency: " + serverStatus_opLatencies_reads_latency)

serverStatus_opLatencies_reads_ops = re.findall(r"\"reads\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_opLatencies_reads_ops = re.findall(r"\d+",serverStatus_opLatencies_reads_ops)[0]
print("Server status oplatencies reads ops: " + serverStatus_opLatencies_reads_ops)

serverStatus_opLatencies_writes_latency = re.findall(r"\"writes\".+(\n.+){1}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_opLatencies_writes_latency = re.findall(r"\d+",serverStatus_opLatencies_writes_latency)[0]
print("Server status oplatencies writes latency: " + serverStatus_opLatencies_writes_latency)

serverStatus_opLatencies_writes_ops = re.findall(r"\"writes\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_opLatencies_writes_ops = re.findall(r"\d+",serverStatus_opLatencies_writes_ops)[0]
print("Server status oplatencies writes ops: " + serverStatus_opLatencies_writes_ops)

serverStatus_cursor_timedOut = re.findall(r"\"timedOut\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_cursor_timedOut = re.findall(r"\d+",serverStatus_cursor_timedOut)[0]
print("Server status cursor timedout: " + serverStatus_cursor_timedOut)

serverStatus_operation_scanAndOrder = re.findall(r"\"scanAndOrder\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_operation_scanAndOrder = re.findall(r"\d+",serverStatus_operation_scanAndOrder)[0]
print("Server status operation scan and order: " + serverops)

serverStatus_operation_writeConflicts = re.findall(r"\"writeConflicts\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
serverStatus_operation_writeConflicts = re.findall(r"\d+",serverStatus_operation_writeConflicts)[0]
print("Server status operation write conflicts: " + serverStatus_operation_writeConflicts)

f.close




