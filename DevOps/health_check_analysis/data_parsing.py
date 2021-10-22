import json
import re
from utils import *

# import mongodb configuration
config_data = open('config.json')
config_json = json.load(config_data)
username = config_json["username"]
password = config_json["password"]
config_path = config_json["mongod_conf"]
health_check_start = config_json["health_check_start"]
health_check_end = config_json["health_check_end"]
company = config_json["company"]
hosts = config_json["hosts"]
health_check_date = config_json["date"]


# read mongod.conf
with open("{}".format(config_path),"r") as config_data:
    try:
        mongod_conf = config_data.read()
    except Exception as e:
        print(e)

mongodb_port = re.findall(r"(port.+)",mongod_conf)[0].split(':')[1].strip()

# check if tls/ssl protocal enable
if re.findall(r"tls:",mongod_conf) != None:
    isTls = True
    tlsCertificateKeyFile = re.findall(r"certificateKeyFile.+",mongod_conf)[0].split(":")[1].strip()
    tlsCAFile = re.findall(r"CAFile.+",mongod_conf)[0].split(":")[1].strip()
    tlsCertificateKeyFilePassword = re.findall(r"certificateKeyFilePassword.+",mongod_conf)[0].split(":")[1].strip()
else:
    isTls = False
    tlsCertificateKeyFile = ""
    tlsCAFile = ""
    tlsCertifacateKeyFilePassword = ""

for host in hosts:
    hostname = host["hostname"]
    mongodb_set = host["mongodb_set"]
    mongod_name = host["mongod_name"]
    input_path = "./{}_health_check_{}".format(hostname,health_check_date)

    # parsing & load health check data
    read_process("""echo "company = '{}'" > ./vars.{}.js""".format(company,hostname))
    read_process("""echo "mongodb_set = '{}'" >> ./vars.{}.js""".format(mongodb_set,hostname))
    read_process("""echo "hostname = '{}'" >> ./vars.{}.js""".format(hostname,hostname))
    read_process("""echo "health_check_start = {}" >> ./vars.{}.js""".format(health_check_start,hostname))
    read_process("""echo "health_check_end = {}" >> ./vars.{}.js""".format(health_check_end,hostname))

    # parsing cpu info
    cpu_info = read_file('{}/cpu-info2.txt'.format(input_path))
    cpu_cores = re.findall(r"^CPU\(s\).+\d",cpu_info,re.M)[0].split(":")[1].strip()
    cpu_model = re.findall(r"^Model name:.+",cpu_info,re.M)[0].split(":")[1].strip()

    ##### FIX hypervisor or physical
    hypervisor = re.findall(r"^Hypervisor.+",cpu_info,re.M)[0].split(":")[1].strip()
    read_process("echo 'cpu_cores = {}' >> ./vars.js".format(cpu_cores))
    read_process("""echo "cpu_model = '{}'" >> ./vars.js""".format(cpu_model))
    read_process("""echo "hypervisor = '{}'" >> ./vars.js""".format(hypervisor))

    # load os version
    os_version = read_file('{}/os-version.txt'.format(input_path))
    read_process("""echo "os_version = '{}'" >> ./vars.js""".format(os_version))

    # parsing & load memory info
    mem_info = read_file('{}/mem-info.txt'.format(input_path))
    mem_space = re.findall(r"^Mem.+",mem_info,re.M)[0].split()[1]
    swap_space = re.findall(r"^Swap.+",mem_info,re.M)[0].split()[1]
    mem_swap = mem_space + '/' + swap_space
    read_process("""echo "mem_swap = '{}'" >> ./vars.js""".format(mem_swap))

    # parsing & load memory info
    disk_info = read_file('{}/disk-info2.txt'.format(input_path))
    home_space_total = re.findall(r".+\/$",disk_info,re.M)[0].split()[1]
    home_space_used = re.findall(r".+\/$",disk_info,re.M)[0].split()[2]
    read_process("""echo "home_space_total = '{}'" >> ./vars.js""".format(home_space_total))
    read_process("""echo "home_space_used = '{}'" >> ./vars.js""".format(home_space_used))

    # load uptime
    uptime = read_file('{}/uptime.txt'.format(input_path))
    read_process("""echo "uptime = '{}'" >> ./vars.js""".format(uptime))

    # parsing & load ulimit info
    ulimit = read_file('{}/ulimit.txt'.format(input_path))
    ulimit_nproc = re.findall(r"^Max processes.+",ulimit,re.M)[0].split()[3]
    ulimit_nofile = re.findall(r"^Max open files.+",ulimit,re.M)[0].split()[4]
    read_process("echo 'ulimit_nproc = {}' >> ./vars.js".format(ulimit_nproc))
    read_process("echo 'ulimit_nofile = {}' >> ./vars.js".format(ulimit_nofile))

    # parsing & load readahead
    readahead = read_file('{}/readahead.txt'.format(input_path))
    readahead = re.findall(r"^rw.+",readahead,re.M)[0].split()[1]
    read_process("echo 'readahead = {}' >> ./vars.js".format(readahead))

    # parsing & check if thp enabled
    thp_enabled = read_file('{}/thp_enabled.txt'.format(input_path))
    if len(re.findall(r"\[never\]",thp_enabled)) > 0:
        thp_enabled_flag = "true"
    else:
        thp_enabled_flag = "false"
    read_process("echo 'thp_enabled_flag = {}' >> ./vars.js".format(thp_enabled_flag))

    path = '{}/thp_defrag.txt'.format(input_path)
    thp_defrag = read_file('{}/thp_defrag.txt'.format(input_path))
    if len(re.findall(r"\[never\]",thp_defrag)) > 0:
        thp_defrag_flag = "true"
    else:
        thp_defrag_flag = "false"
    read_process("echo 'thp_defrag_flag = {}' >> ./vars.js".format(thp_defrag_flag))

    # parsing & check if selinux enabled
    selinux = read_file('{}/selinux.txt'.format(input_path))
    isSelinux = "false" if re.findall(r"^SELINUX.+",selinux,re.M)[0].split("=")[1] == "disabled" else "true"
    read_process("echo 'isSelinux = {}' >> ./vars.js".format(isSelinux))

    # parsing & load vm zone reclaim mode
    vm_zone_reclaim_mode = read_file('{}/vm_zone_reclaim_mode.txt'.format(input_path))
    read_process("echo 'vm_zone_reclaim_mode = {}' >> ./vars.js".format(vm_zone_reclaim_mode))

    # parsing & load vm swappiness
    vm_swappiness = read_file('{}/vm_swappiness.txt'.format(input_path))
    read_process("echo 'vm_swappiness = {}' >> ./vars.js".format(vm_swappiness))

    # parsing & load mongodb version
    mongodb_version = read_file('{}/mongodb_version.txt'.format(input_path))
    mongodb_version = re.findall(r"v[\d.]+",mongodb_version)[0]
    read_process("""echo "mongodb_version = '{}'" >> ./vars.js""".format(mongodb_version))

    # parsing & load mongodb fcv
    mongodb_fcv = read_file('{}/{}/mongodb_fcv.txt'.format(input_path,mongod_name))
    mongodb_fcv = re.findall(r"version.+",mongodb_fcv)[0].split(":")[1].strip().strip("\"")
    read_process("""echo "mongodb_fcv = '{}'" >> ./vars.js""".format(mongodb_fcv))

    # parsing & load mongodb port
    mongodb_port = read_file('{}/mongodb_port.txt'.format(input_path))
    read_process("echo 'mongodb_port = {}' >> ./vars.js".format(mongodb_port))

    # parsing & load server status info
    mongodb_serverStatus = read_file('{}/{}/mongodb_serverStatus.txt'.format(input_path,mongod_name))

    serverStatus_uptime = re.findall(r"\"uptime\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    read_process("echo 'serverStatus_uptime = {}' >> ./vars.js".format(serverStatus_uptime))

    serverStatus_asserts_warning = re.findall(r"\"warning\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    read_process("echo 'serverStatus_asserts_warning = {}' >> ./vars.js".format(serverStatus_asserts_warning))

    serverStatus_asserts_user = re.findall(r"\"user\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    read_process("echo 'serverStatus_asserts_user = {}' >> ./vars.js".format(serverStatus_asserts_user))

    serverStatus_connections_current = re.findall(r"\"connections\"(.+\n){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    read_process("echo 'serverStatus_connection_current = {}' >> ./vars.js".format(serverStatus_connections_current))

    serverStatus_connections_available = re.findall(r"\"connections\"(.+\n){3}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    read_process("echo 'serverStatus_connections_available = {}' >> ./vars.js".format(serverStatus_connections_available))

    serverStatus_extra_info_page_faults = re.findall(r"\"page_faults\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_extra_info_page_faults = re.findall(r"\d+",serverStatus_extra_info_page_faults)[0]
    read_process("echo 'serverStatus_extra_info_page_faults = {}' >> ./vars.js".format(serverStatus_extra_info_page_faults))

    serverStatus_opLatencies_reads_latency = re.findall(r"\"reads\".+(\n.+){1}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_opLatencies_reads_latency = re.findall(r"\d+",serverStatus_opLatencies_reads_latency)[0]
    read_process("echo 'serverStatus_opLatencies_reads_latency = {}' >> ./vars.js".format(serverStatus_opLatencies_reads_latency))

    serverStatus_opLatencies_reads_ops = re.findall(r"\"reads\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_opLatencies_reads_ops = re.findall(r"\d+",serverStatus_opLatencies_reads_ops)[0]
    read_process("echo 'serverStatus_opLatencies_reads_ops = {}' >> ./vars.js".format(serverStatus_opLatencies_reads_ops))

    serverStatus_opLatencies_writes_latency = re.findall(r"\"writes\".+(\n.+){1}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_opLatencies_writes_latency = re.findall(r"\d+",serverStatus_opLatencies_writes_latency)[0]
    read_process("echo 'serverStatus_opLatencies_writes_latency = {}' >> ./vars.js".format(serverStatus_opLatencies_writes_latency))

    serverStatus_opLatencies_writes_ops = re.findall(r"\"writes\".+(\n.+){2}",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_opLatencies_writes_ops = re.findall(r"\d+",serverStatus_opLatencies_writes_ops)[0]
    read_process("echo 'serverStatus_opLatencies_writes_ops = {}' >> ./vars.js".format(serverStatus_opLatencies_writes_ops))

    serverStatus_cursor_timedOut = re.findall(r"\"timedOut\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_cursor_timedOut = re.findall(r"\d+",serverStatus_cursor_timedOut)[0]
    read_process("echo 'serverStatus_cursor_timedOut = {}' >> ./vars.js".format(serverStatus_cursor_timedOut))

    serverStatus_operation_scanAndOrder = re.findall(r"\"scanAndOrder\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_operation_scanAndOrder = re.findall(r"\d+",serverStatus_operation_scanAndOrder)[0]
    read_process("echo 'serverStatus_operation_scanAndOrder = {}' >> ./vars.js".format(serverStatus_operation_scanAndOrder))

    serverStatus_operation_writeConflicts = re.findall(r"\"writeConflicts\".+",mongodb_serverStatus)[0].split(":")[1].strip().strip(',')
    serverStatus_operation_writeConflicts = re.findall(r"\d+",serverStatus_operation_writeConflicts)[0]
    read_process("echo 'serverStatus_operation_writeConflicts = {}' >> ./vars.js".format(serverStatus_operation_writeConflicts))

    mongodb_rs_conf = read_file('{}/{}/mongodb_rs_conf.txt'.format(input_path,mongod_name))
    mongodb_rs_conf = re.sub(r"\"","\"",mongodb_rs_conf,0)
    read_process("echo 'mongodb_rs_conf = {};' >> ./vars.js".format(mongodb_rs_conf))

    # dump linux config data into mongodb
    output_linux_config_dump = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        js="linux_config_dump.js")

    # dump server status data into mongodb
    output_server_status_dump = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        js="server_status_dump.js")

    # parsing & dump mongodb dbs status into mongodb
    mongodb_dbstats = read_file('{}/{}/mongodb_dbstats.txt'.format(input_path,mongod_name))
    mongodb_dbstats = re.sub(r"\"\$clusterTime\"(.+\n){7}","",mongodb_dbstats)
    mongodb_dbstats = re.sub(r"loading.+","",mongodb_dbstats,0)
    read_process("echo '{}' > {}/{}/mongodb_dbstats.json".format(mongodb_dbstats,input_path,mongod_name))

    mongoimport(port=mongodb_port,\
        username=username, \
        password=password, \
        db=company, \
        collection="db_stats", \
        file="'{}/{}/mongodb_dbstats.json'".format(input_path,mongod_name), \
        isTls=isTls, \
        tlsCAFile=tlsCAFile, \
        tlsCertificateKeyFile=tlsCertificateKeyFile, \
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword)

    # parsing & dump mongodb collections status into mongodb
    mongodb_collstats = read_file('{}/{}/mongodb_collstats.txt'.format(input_path,mongod_name))
    mongodb_collstats = re.sub(r"\"\$clusterTime\"(.+\n){7}","",mongodb_collstats)
    mongodb_collstats = re.sub(r"loading.+","",mongodb_collstats,0)
    f = open("{}/{}/mongodb_collstats.json".format(input_path,mongod_name),"w+")
    f.write(mongodb_collstats)
    f.close()

    mongoimport(port=mongodb_port, \
        username=username, \
        password=password, \
        db=company, \
        collection="coll_stats", \
        file="'{}/{}/mongodb_collstats.json'".format(input_path,mongod_name), \
        isTls=isTls, \
        tlsCAFile=tlsCAFile, \
        tlsCertificateKeyFile=tlsCertificateKeyFile, \
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword)

    # parsing & dump collection fragmentaion info into mongodb
    mongodb_rs_frag = read_file('{}/{}/mongodb_rs_frag.txt'.format(input_path,mongod_name))
    mongodb_rs_frag = re.sub(r"loading.+","",mongodb_rs_frag,0)
    mongodb_rs_frag = re.sub(r"\"","\\\"",mongodb_rs_frag,0)
    read_process("""echo "mongodb_rs_frag = {}" >> ./vars.js""".format(mongodb_rs_frag))

    output_mongodb_rs_frag = mongosh(port=mongodb_port,\
        username=username,\
        password=password,\
        isTls=isTls,\
        tlsCAFile=tlsCAFile,\
        tlsCertificateKeyFile=tlsCertificateKeyFile,\
        tlsCertificateKeyFilePassword=tlsCertificateKeyFilePassword,\
        js="addFields.js")