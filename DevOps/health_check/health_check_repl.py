import os
import re
from datetime import date

def read_process(cmd, args=''):
    fullcmd = '%s %s' % (cmd, args)
    pipeout = os.popen(fullcmd)
    try:
        firstline = pipeout.readline()
        cmd_not_found = re.search(
            b'(not recognized|No such file|not found)',
            firstline,
            re.IGNORECASE
        )
        if cmd_not_found:
            raise IOError('%s must be on your system path.' % cmd)
        output = firstline + pipeout.read()
    finally:
        pipeout.close()
    return output

# script config
today = date.today()
output_dir = "health_check_{}".format(today)
output_path = "./{}".format(output_dir)
mongodb_port = 27017
config_path = "/etc/mongod.conf"
username = "admin"
password = "admin"

# linux info
output_mkdir = read_process("mkdir {}".format(output_dir))
output_osVersion = read_process("cat /etc/redhat-release > {}/os-version.txt".format(output_path))
output_cpu_info = read_process("cat /proc/cpuinfo > {}/cpu-info.txt".format(output_path))
output_cpu_info2 = read_process("lscpu >> {}/cpu-info.txt".format(output_path))
output_mem_info = read_process("free -h > {}/mem-info.txt".format(output_path))
output_disk_info_block = read_process("lsblk > {}/disk-info.txt".format(output_path))
output_disk_info_fs = read_process("df -h >> {}/disk-info.txt".format(output_path))
output_network_info = read_process("ip addr > {}/network-info.txt".format(output_path))
output_uptime = read_process("uptime > {}/uptime.txt".format(output_path))
output_numa = read_process("numactl --hardware > {}/numa.txt".format(output_path))
output_numa = read_process("cat /proc/cmdline >> {}/numa.txt".format(output_path))
output_numa = read_process("dmesg | grep -i numa >> {}/numa.txt".format(output_path))
output_thp_defrag = read_process("cat /sys/kernel/mm/transparent_hugepage/defrag > {}/thp_defrag.txt".format(output_path))
output_thp_enabled = read_process("cat /sys/kernel/mm/transparent_hugepage/enabled > {}/thp_enabled.txt".format(output_path))
output_noatime = read_process("cat /etc/fstab > {}/noatime.txt".format(output_path))
output_vm_swappiness = read_process("cat /proc/sys/vm/swappiness > {}/vm_swappiness.txt".format(output_path))
output_ntpstat = read_process("ntpstat > {}/ntpstat.txt".format(output_path))
output_mongodb_config = read_process("cat {} > {}/mongodb_conf.txt".format(config_path,output_path))

# mongo instance info
output_mongodb_version = read_process("mongod -version > {}/mongodb_version.txt".format(output_path))
output_mongodb_serverStatus = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.serverStatus()' > {}/mongodb_serverStatus.txt".format(mongodb_port,username,password,output_path))
output_mongodb_dbstats = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin ./get_dbstats.js > {}/mongodb_dbstats.txt".format(mongodb_port,username,password,output_path))
output_mongodb_rs_conf = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin --eval 'rs.conf()' > {}/mongodb_rs_conf.txt".format(mongodb_port,username,password,output_path))
output_mongodb_rs_status = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin --eval 'rs.status()' > {}/mongodb_rs_status.txt".format(mongodb_port,username,password,output_path))
output_mongodb_rs_oplog = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.getReplicationInfo()' > {}/mongodb_rs_oplog.txt".format(mongodb_port,username,password,output_path))
output_mongodb_rs_lagtime = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin --eval 'db.printSecondaryReplicationInfo()' > {}/mongodb_rs_lagtime.txt".format(mongodb_port,username,password,output_path))
output_mongodb_rs_frag = read_process("mongo -port {} -u {} -p {} --authenticationDatabase admin ./get_colls_frag_ratio.js > {}/mongodb_rs_frag.txt".format(mongodb_port,username,password,output_path))

# compress output files
output_compression = read_process("tar zcvf {}.tar.gz {}".format(output_dir, output_dir))
output_remove_dir = read_process("rm -rf {}".format(output_dir))