import utils

mongodump = """
mongodump \ 
    -u {{ mongodb_admin_user }} \
    -p {{ mongodb_admin_pwd }} \
    --authenticationDatabase=admin \
    --port {{ mongodb_port }} \
    -o /opt/OmniMongoDB/backup/{{ ansible_date_time.date }}_mongodb_backup
"""

mongosh = """
mongo \
    -u admin\
    -p admin\
    --authenticationDatabase=admin \
    --port 27017 \
    --eval
"""

utils.read_process("{} {}".format(mongosh,"`db.fsyncLock();`"))

utils.read_process("{}".format(mongodump))

utils.read_process("{} {}".format(mongosh,"`db.fsyncUnlock();`"))