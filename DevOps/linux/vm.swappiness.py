from utils import *
import os
import re

def setup_vm_swappiness():

    # ensure sysctl.conf path exists
    if(os.path.isfile("/etc/sysctl.conf") == False):
        print("Fatal Error: sysctl.conf file does not exist, please checkout.")
        exit()
    else:
        with open('/etc/sysctl.conf', 'r') as sysconf_file :
            sysconf = sysconf_file.read()
        print("Message: sysctl.conf file check completed successfully.")

    read_process("echo 1 > /proc/sys/vm/swappiness")

    if(re.search(r"vm.swappiness.+",sysconf)):
        sysconf = re.sub(r"vm.swappiness.+","vm.swappiness=1",sysconf)
        with open('/etc/sysctl.conf', 'w') as sysconf_file:
            sysconf_file.write(sysconf)
    else:
        read_process("echo 'vm.swappiness=1' >> /etc/sysctl.conf")

    print("vm.swappiness=" + read_process("cat /proc/sys/vm/swappiness"))
