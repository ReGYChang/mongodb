import re
import sys
import json
from datetime import date
from subprocess import check_output
from utils import *

# script config
today = date.today()
hostname = read_process("hostname").strip()
output_dir = "{}_health_check_{}".format(hostname,today)
output_path = "./{}".format(output_dir)
mongod_pid = check_output(["pidof","-s","mongod"]).strip()

# create health check dir
read_process("mkdir {}".format(output_dir))

# linux info
# output_osVersion = read_process("cat /etc/redhat-release > {}/os-version.txt".format(output_path))
# output_cpu_info = read_process("cat /proc/cpuinfo > {}/cpu-info.txt".format(output_path))
# output_cpu_info2 = read_process("lscpu >> {}/cpu-info.txt".format(output_path))
# output_ps_mem = read_process("ps aux --sort -rss | head")
# output_ps_cpu = read_process("ps aux --sort -pcpu | head")
# output_mem_info = read_process("free -h > {}/mem-info.txt".format(output_path))
# output_disk_info_block = read_process("lsblk > {}/disk-info.txt".format(output_path))
# output_disk_info_fs = read_process("df -h >> {}/disk-info.txt".format(output_path))
# output_network_info = read_process("ip addr > {}/network-info.txt".format(output_path))
# output_uptime = read_process("uptime > {}/uptime.txt".format(output_path))
# output_numa = read_process("cat /proc/cmdline >> {}/numa.txt".format(output_path))
# output_numa = read_process("dmesg | grep -i numa >> {}/numa.txt".format(output_path))
# output_thp_defrag = read_process("cat /sys/kernel/mm/transparent_hugepage/defrag > {}/thp_defrag.txt".format(output_path))
# output_thp_enabled = read_process("cat /sys/kernel/mm/transparent_hugepage/enabled > {}/thp_enabled.txt".format(output_path))
# output_noatime = read_process("cat /etc/fstab > {}/noatime.txt".format(output_path))
# output_vm_swappiness = read_process("cat /proc/sys/vm/swappiness > {}/vm_swappiness.txt".format(output_path))
# output_vm_zone_reclaim_mode = read_process("cat /proc/sys/vm/zone_reclaim_mode > {}/vm_zone_reclaim_mode.txt".format(output_path))
# output_readahead = read_process("blockdev --report > {}/readahead.txt".format(output_path))
# output_selinux = read_process("cat /etc/selinux/config > {}/selinux.txt".format(output_path))
#output_crontab = read_process("crontab -u mongod -l")
# output_ulimit = read_process("cat /proc/{}/limits > {}/ulimit.txt".format(mongod_pid,output_path))

output_osVersion = bashsh(cmd="cat",\
        args=["/etc/redhat-release"],\
        output_path=output_path,\
        task_name="os-version",\
        append=False)

output_cpu_info = bashsh(cmd="cat",\
        args=["/proc/cpuinfo"],\
        output_path=output_path,\
        task_name="cpu-info",\
        append=False)

output_cpu_info2 = bashsh(cmd="lscpu",\
        args=[""],\
        output_path=output_path,\
        task_name="cpu-info",\
        append=True)

output_ps_mem = bashsh(cmd="ps",\
        args=["aux","--sort","-rss","| head"],\
        output_path=output_path,\
        task_name="ps-mem",\
        append=False)

output_ps_cpu = bashsh(cmd="ps",\
        args=["aux","--sort","-pcpu","| head"],\
        output_path=output_path,\
        task_name="ps-cpu",\
        append=False)

output_mem_info = bashsh(cmd="free",\
        args=["-h"],\
        output_path=output_path,\
        task_name="mem-info",\
        append=False)

output_disk_info_block = bashsh(cmd="lsblk",\
        args=[""],\
        output_path=output_path,\
        task_name="disk-info",\
        append=False)

output_disk_info_fs = bashsh(cmd="df",\
        args=["-h"],\
        output_path=output_path,\
        task_name="disk-info",\
        append=True)

output_network_info = bashsh(cmd="ip addr",\
        args=[""],\
        output_path=output_path,\
        task_name="network-info",\
        append=False)

output_uptime = bashsh(cmd="uptime",\
        args=[""],\
        output_path=output_path,\
        task_name="uptime",\
        append=False)

output_numa_info = bashsh(cmd="cat",\
        args=["/proc/cmdline"],\
        output_path=output_path,\
        task_name="numa1",\
        append=False)

output_numa_info2 = bashsh(cmd="dmesg",\
        args=["| grep -i numa"],\
        output_path=output_path,\
        task_name="numa2",\
        append=True)

output_thp_defrag = bashsh(cmd="cat",\
        args=["/sys/kernel/mm/transparent_hugepage/defrag"],\
        output_path=output_path,\
        task_name="thp_defrag",\
        append=False)

output_thp_enabled = bashsh(cmd="cat",\
        args=["/sys/kernel/mm/transparent_hugepage/enabled"],\
        output_path=output_path,\
        task_name="thp_enabled",\
        append=False)

output_noatime = bashsh(cmd="cat",\
        args=["/etc/fstab"],\
        output_path=output_path,\
        task_name="noatime",\
        append=False)

output_vm_swappiness = bashsh(cmd="cat",\
        args=["/proc/sys/vm/swappiness"],\
        output_path=output_path,\
        task_name="vm_swappiness",\
        append=False)

output_vm_zone_reclaim_mode = bashsh(cmd="cat",\
        args=["/proc/sys/vm/zone_reclaim_mode"],\
        output_path=output_path,\
        task_name="vm_zone_reclaim_mode",\
        append=False)

output_readahead = bashsh(cmd="blockdev",\
        args=["--report"],\
        output_path=output_path,\
        task_name="readahead",\
        append=False)

output_selinux = bashsh(cmd="cat",\
        args=["/etc/selinux/config"],\
        output_path=output_path,\
        task_name="selinux",\
        append=False)

output_ulimit = bashsh(cmd="cat",\
        args=["/proc/{}/limits".format(mongod_pid)],\
        output_path=output_path,\
        task_name="ulimit",\
        append=False)

# import configuration
config_data = open('config.json')
config_json = json.load(config_data)
mongo_hosts = config_json["hosts"]

for host in mongo_hosts:
    config_path = host["mongod_conf"]
    mongod_name = host["name"]
    username = host["username"]
    password = host["password"]

    read_process("mkdir -p {}/{}".format(output_dir,mongod_name))

    # read mongod.conf
    with open("{}".format(config_path),"r") as config_data:
        try:
            mongod_conf = config_data.read()
        except Exception as e:
            print(e)

    log_path = re.findall(r"(path.+)",mongod_conf)[0].split(':')[1].strip()
    mongodb_port = re.findall(r"(port.+)",mongod_conf)[0].split(':')[1].strip()
    mongod_version = re.findall(r"(v[\d.]+)",read_process("mongod --version"))[0].split('.')[1].strip()

    if re.findall(r"tls",mongod_conf,re.I) != None:
        isTls = True
        tlsCertificateKeyFile = re.findall(r"certificateKeyFile.+",mongod_conf)[0].split(":")[1].strip()
        tlsCAFile = re.findall(r"CAFile.+",mongod_conf)[0].split(":")[1].strip()
        tlsCertificateKeyFilePassword = re.findall(r"certificateKeyFilePassword.+",mongod_conf)[0].split(":")[1].strip()
    else:
        isTls = False
        tlsCertificateKeyFile = ""
        tlsCAFile = ""
        tlsCertifacateKeyFilePassword = ""

    read_process("echo 'version = {}' > ./vars.js".format(mongod_version))

    # mongo instance info
    # output_mongodb_config = read_process("cat {} > {}/mongod_conf.txt".format(config_path,output_path))
    # output_mongodb_version = read_process("/usr/bin/mongod -version > {}/mongodb_version.txt".format(output_path))
    
    output_mongodb_config = bashsh(cmd="cat",\
        args=[config_path],\
        output_path=output_path,\
        task_name="mongodb_config",\
        append=False)

    output_mongodb_version = bashsh(cmd="/usr/bin/mongod",\
        args=["-version"],\
        output_path=output_path,\
        task_name="mongodb_version",\
        append=False)
    
    output_mongodb_serverStatus = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=True,\
        cmd="db.serverStatus()",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_serverStatus")

    output_mongodb_rs_conf = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=True,\
        cmd="rs.conf()",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_rs_conf")

    output_mongodb_rs_status = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=True,\
        cmd="rs.status()",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_rs_status")

    output_mongodb_rs_oplog = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=True,\
        cmd="db.getReplicationInfo()",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_rs_oplog")

    output_mongodb_fcv = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_fcv.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_fcv")

    output_mongodb_dbstats = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_dbstats.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_dbstats")

    output_mongodb_rs_frag = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_colls_frag_ratio.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_rs_frag")

    output_mongodb_colls_stats = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_colls_stats.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_colls_stats")

    output_mongodb_indexes = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_indexes.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_indexes")

    output_mongodb_rs_lagtime = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        isEval=False,\
        js="get_rs_lagtime.js",\
        output_path=output_path,\
        mongod_name=mongod_name,\
        task_name="mongodb_rs_lagtime")

# cp mongod.log
#read_process("cp {} {}/mongod.log.{}".format(log_path,output_path,today))

# compress output files
output_compression = read_process("tar zcvf {}.tar.gz {}".format(output_dir, output_dir))

# health check end
sys.stdout.write('\n')
sys.stdout.flush()
