import os
import re
import datetime

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

def getPrimaryNode(port):
    primary = read_process("mongo --quiet \
        --port {} \
        --eval 'db.hello().primary'".format(port))
    return primary.split(':')[0]

def getSecondaryNode(port):
    hosts = read_process("mongo \
        --quiet \
        --port {} \
        --eval 'db.hello().hosts'".format(port))

    primary = read_process("mongo \
        --quiet \
        --port {} \
        --eval 'db.hello().primary'".format(port))

    for host in re.findall(r"\"(.+?)\"",hosts):
        if primary == host:
            continue
        return host.split(':')[0]

def getCurrentDate():
    return datetime.date.today()

def getCurrentHour():
    return read_process("date -d '-1 days' '+%Y%m%d%H'")

def mongodump(host,username,password,port,output,isGzip,*isOplog):
    dump_args = "mongodump \
        --host {} \
        -u {} \
        -p {} \
        --port {} \
        -o {} \
        --authenticationDatabase=admin".format(host,username,password,port,output)
    if isGzip:
        dump_args += " \\n--gzip"
    if isOplog[0]:
        dump_args += " \n-d local \
            -c oplog.rs \
            --query '{ts:{$gte:Timestamp({},1),$lte:Timestamp({},9999)}}'".format(isOplog[1],isOplog[2])
    read_process(dump_args)