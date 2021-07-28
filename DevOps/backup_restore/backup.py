from utils import *

mongodump = """
mongodump \ 
    -u admin \
    -p admin \
    --authenticationDatabase=admin \
    --port 27017 \
    -o /opt/OmniMongoDB/backup/{}_mongodb_backup
""".format(getCurrentDate())

mongosh = """
mongo \
    --host {}
    -u admin\
    -p admin\
    --authenticationDatabase=admin \
    --port 27017 \
    --eval
""".format(getSecondaryNode())

read_process("{} {}".format(mongosh,"'db.fsyncLock();'"))

read_process("{}".format(mongodump))

read_process("{} {}".format(mongosh,"'db.fsyncUnlock();'"))