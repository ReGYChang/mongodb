import re
import sys
import json
from datetime import date
from subprocess import check_output
from utils import *

toolbar_width = 30

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['


def pb_flush():
    sys.stdout.write("#")
    sys.stdout.flush()

# script config
today = date.today()
hostname = read_process("hostname").strip()
output_dir = "{}_health_check_{}".format(hostname,today)
output_path = "./{}".format(output_dir)

# linux info
output_mkdir = read_process("mkdir {}".format(output_dir))
output_osVersion = read_process("cat /etc/redhat-release > {}/os-version.txt".format(output_path))
output_cpu_info = read_process("cat /proc/cpuinfo > {}/cpu-info.txt".format(output_path))
output_cpu_info2 = read_process("lscpu >> {}/cpu-info.txt".format(output_path))
output_ps_mem = read_process("ps aux --sort -rss | head")
output_ps_cpu = read_process("ps aux --sort -pcpu | head")
output_mem_info = read_process("free -h > {}/mem-info.txt".format(output_path))
output_disk_info_block = read_process("lsblk > {}/disk-info.txt".format(output_path))
output_disk_info_fs = read_process("df -h >> {}/disk-info.txt".format(output_path))
output_network_info = read_process("ip addr > {}/network-info.txt".format(output_path))
output_uptime = read_process("uptime > {}/uptime.txt".format(output_path))
output_numa = read_process("cat /proc/cmdline >> {}/numa.txt".format(output_path))
output_numa = read_process("dmesg | grep -i numa >> {}/numa.txt".format(output_path))
output_thp_defrag = read_process("cat /sys/kernel/mm/transparent_hugepage/defrag > {}/thp_defrag.txt".format(output_path))
output_thp_enabled = read_process("cat /sys/kernel/mm/transparent_hugepage/enabled > {}/thp_enabled.txt".format(output_path))
output_noatime = read_process("cat /etc/fstab > {}/noatime.txt".format(output_path))
output_vm_swappiness = read_process("cat /proc/sys/vm/swappiness > {}/vm_swappiness.txt".format(output_path))
output_vm_zone_reclaim_mode = read_process("cat /proc/sys/vm/zone_reclaim_mode > {}/vm_zone_reclaim_mode.txt".format(output_path))
output_readahead = read_process("blockdev --report > {}/readahead.txt".format(output_path))
output_ntpstat = read_process("ntpstat > {}/ntpstat.txt".format(output_path))
output_crontab = read_process("crontab -u mongod -l")
output_ulimit = read_process("cat /proc/{}/limits > {}/ulimit.txt".format(mongod_pid,output_path))

# import configuration
config_data = open('config.json')
config_json = json.load(config_data)

mongo_hosts = config_json["hosts"]

for host in mongo_hosts:
    config_path = host["mongod_conf"]
    mongod_name = host["name"]
    username = host["username"]
    password = host["password"]

    read_process("mkdir {}/{}".format(output_dir,mongod_name))

    # read mongod.conf
    with open("{}".format(config_path),"r") as config_data:
        try:
            mongod_conf = config_data.read()
        except Exception as e:
            print(e)

    log_path = re.findall(r"(path.+)",mongod_conf)[0].split(':')[1].strip()
    mongodb_port = re.findall(r"(port.+)",mongod_conf)[0].split(':')[1].strip()
    mongod_pid = check_output(["pidof","-s","mongod"]).strip()
    mongod_version = re.findall(r"(v[\d.]+)",read_process("mongod --version"))[0].split('.')[1].strip()

    read_process("echo 'version = {}' > ./vars.js".format(mongod_version))

    # mongo instance info
    output_mongodb_config = read_process("cat {} > {}/mongod_conf.txt".format(config_path,output_path))
    output_mongodb_version = read_process("/usr/bin/mongod -version > {}/mongodb_version.txt".format(output_path))
    output_mongodb_serverStatus = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.serverStatus()' > {}/{}/mongodb_serverStatus.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_rs_conf = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'rs.conf()' > {}/{}/mongodb_rs_conf.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_rs_status = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'rs.status()' > {}/{}/mongodb_rs_status.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_rs_oplog = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.getReplicationInfo()' > {}/{}/mongodb_rs_oplog.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_fcv = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin ./vars.js ./get_fcv.js > {}/{}/mongodb_fcv.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_dbstats = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin ./vars.js ./get_dbstats.js > {}/{}/mongodb_dbstats.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_rs_frag = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin ./vars.js ./get_colls_frag_ratio.js > {}/{}/mongodb_rs_frag.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_colls_stats = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin ./vars.js ./get_colls_stats.js > {}/{}/mongodb_colls_stats.txt".format(mongodb_port,username,password,output_path,mongod_name))
    output_mongodb_indexes = read_process("/usr/bin/mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin ./vars.js ./get_indexes.js > {}/{}/mongodb_indexes.txt".format(mongodb_port,username,password,output_path,mongod_name))

    if int(mongod_version) <= 2:
        output_mongodb_rs_lagtime = read_process("mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.printSlaveReplicationInfo()' > {}/{}/mongodb_rs_lagtime.txt".format(mongodb_port,username,password,output_path,mongod_name))
    else:
        output_mongodb_rs_lagtime = read_process("mongo --quiet -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.printSecondaryReplicationInfo()' > {}/{}/mongodb_rs_lagtime.txt".format(mongodb_port,username,password,output_path,mongod_name))

# cp mongod.log
#read_process("cp {} {}/mongod.log.{}".format(log_path,output_path,today))

# compress output files
output_compression = read_process("tar zcvf {}.tar.gz {}".format(output_dir, output_dir))

sys.stdout.write("]\n") # this ends the progress bar
