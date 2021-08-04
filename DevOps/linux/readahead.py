from utils import *
import os
import re

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

    read_process("service tuned restart")

    print(read_process("blockdev --report"))