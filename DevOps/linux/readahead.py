from utils import *
import os
import re

device = "/dev/mapper/vgdata-mongodata"

def setup_readahead():

     # ensure tuned.conf path exists
    if(os.path.isfile("/lib/tuned/throughput-performance/tuned.conf") == False):
        print("Fatal Error: tuned.conf file does not exist, please checkout.")
        exit()
    else:
        with open('/lib/tuned/throughput-performance/tuned.conf', 'r') as tunedconf_file :
            tunedconf = tunedconf_file.read()
        print("Message: tuned.conf file check completed successfully.")

    with open('/lib/tuned/throughput-performance/tuned.conf', 'w') as tunedconf_file:
        tunedconf = re.sub(r"readahead=>.+","readahead=>16",tunedconf)
        tunedconf_file.write(tunedconf)

    with open('/etc/rc.d/rc.local', 'r') as rc_local_file :
        rc_local = rc_local_file.read()

    if(re.search(r".+blockdev --setra",rc_local) == None):
        read_process("echo '/sbin/blockdev --setra 32 {}' >> /etc/rc.d/rc.local".format(device))

    read_process("service tuned restart")

    read_process("blockdev --setra 32 /dev/mapper/vgdata-mongodata")

    read_process("chmod +x /etc/rc.d/rc.local")

    print(read_process("blockdev --report"))