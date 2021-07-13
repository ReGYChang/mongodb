import os
import re

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

# js
# get all dbs stats
get_alldbs_dbstats = """
    var alldbs = db.getMongo().getDBNames();
    for(var j = 0; j < alldbs.length; j++){
        var db = db.getSiblingDB(alldbs[j]);
        printjson(db.stats());
    }
"""

# get all collections space fragmentation ratio
get_colls_frag_ratio = """
    function getCollectionDiskSpaceFragRatio(dbname, coll) {
        var res = db.getSiblingDB(dbname).runCommand({
            collStats: coll
        });
        var totalStorageUnusedSize = 0;
        var totalStorageSize = res['storageSize'] + res['totalIndexSize'];
        Object.keys(res.indexDetails).forEach(function(key) {
            var size = res['indexDetails'][key]['block-manager']['file bytes available for reuse'];
            print("index table " + key + " unused size: " + size);
            totalStorageUnusedSize += size;
        });
        var size = res['wiredTiger']['block-manager']['file bytes available for reuse'];
        print("collection table " + coll + " unused size: " + size);
        totalStorageUnusedSize += size;
        print("collection and index table total unused size: " + totalStorageUnusedSize);
        print("collection and index table total file size: " + totalStorageSize);
        print("Fragmentation ratio: " + ((totalStorageUnusedSize * 100.0) / totalStorageSize).toFixed(2) + "%");
    }
    var alldbs = db.getMongo().getDBNames();
    for(var j = 0; j < alldbs.length; j++){
        var db = db.getSiblingDB(alldbs[j]);
        print("\n\n================================== DB: " + db.getName() + " ==================================")
        db.getCollectionNames().forEach((c) => {print("\n\n" + c); getCollectionDiskSpaceFragRatio(db.getName(), c);});
    }
"""

output_dir = "health_check"
output_path = "./{}".format(output_dir)
mongodb_port = 27017
config_path = "/etc/mongod.conf"

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
output_mongodb_version = read_process("mongod -version > {}/mongodb_version.txt".format(output_path))
output_mongodb_fcv = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } )' > {}/mongodb_version.txt".format(output_path))
output_mongodb_serverStatus = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'db.serverStatus()' > {}/mongodb_serverStatus.txt".format(output_path))
output_mongodb_dbstats = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval '{}' > {}/mongodb_dbstats.txt".format(get_alldbs_dbstats,output_path))
output_mongodb_rs_conf = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'rs.conf()' > {}/mongodb_rs_conf.txt".format(output_path))
output_mongodb_rs_status = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'rs.status()' > {}/mongodb_rs_status.txt".format(output_path))
output_mongodb_rs_oplog = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'db.getReplicationInfo()' > {}/mongodb_rs_oplog.txt".format(output_path))
output_mongodb_rs_lagtime = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval 'db.printSecondaryReplicationInfo()' > {}/mongodb_rs_lagtime.txt".format(output_path))
output_mongodb_rs_frag = read_process("mongo -u admin -p admin --authenticationDatabase admin --eval '{}' > {}/mongodb_rs_frag.txt".format(get_colls_frag_ratio,output_path))
