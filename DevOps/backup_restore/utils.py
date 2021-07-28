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
        -- port {} \
        --eval 'db.hello().primary'".format(port))
    return primary.split(':')[0]

def getSecondaryNode(port):
    hosts = read_process("mongo \
        --quiet \
        -- port {} \
        --eval 'db.hello().hosts'".format(port))

    primary = read_process("mongo --quiet \
        -- port {} \
        --eval 'db.hello().primary'".format(port))

    for host in re.findall(r"\"(.+?)\"",hosts):
        if primary == host:
            continue
        return host.split(':')[0]

def getCurrentDate():
    return datetime.date.today()

def getCurrentHour():
    return getCurrentDate().strftime("%Y/%m/%d%H")