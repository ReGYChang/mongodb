import re
import sys
import json
from datetime import date
from subprocess import check_output
from utils import *

# import script config
health_check_date = date.today()
hostname = read_process("hostname").strip()
output_dir = "{}_health_check_{}".format(hostname,health_check_date)
output_path = "./{}".format(output_dir)
mongod_pid = check_output(["pidof","-s","mongod"]).strip()

# create health check dir
read_process("mkdir {}".format(output_dir))

# collect linux info
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
        task_name="cpu-info2",\
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
        task_name="disk-info2",\
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

# import mongodb configuration
config_data = open('config.json')
config_json = json.load(config_data)
mongo_hosts = config_json["hosts"]

for host in mongo_hosts:
    config_path = host["mongod_conf"]
    mongod_name = host["mongod_name"]
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
    mongod_version = re.findall(r"(v[\d.]+)",read_process("/usr/bin/mongod --version"))[0].split('.')[1].strip()

    if len(re.findall(r"tls:",mongod_conf)) > 0:
        isTls = True
        tlsCertificateKeyFile = re.findall(r"certificateKeyFile.+",mongod_conf)[0].split(":")[1].strip()
        tlsCAFile = re.findall(r"CAFile.+",mongod_conf)[0].split(":")[1].strip()
        tlsCertificateKeyFilePassword = re.findall(r"certificateKeyFilePassword.+",mongod_conf)[0].split(":")[1].strip()
    else:
        isTls = False
        tlsCertificateKeyFile = ""
        tlsCAFile = ""
        tlsCertificateKeyFilePassword = ""

    read_process("echo 'version = {}' > ./vars.js".format(mongod_version))

    # collect mongo instance info
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

    output_mongodb_port = bashsh(cmd="echo",\
        args=[mongodb_port],\
        output_path=output_path,\
        task_name="mongodb_port",\
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
        task_name="mongodb_collstats")

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

# compress output health check files
output_compression = read_process("tar zcvf {}.tar.gz {}".format(output_dir, output_dir))

# health check end
sys.stdout.write('\n')
sys.stdout.flush()
