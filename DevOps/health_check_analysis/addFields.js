var db = db.getSiblingDB(company);
var ts = (new Date()).getTime();

// add host to coll_stats docs
db.coll_stats.update({ $and: [{ host: { $exists: false } }, { operationTime: { $gte: Timestamp(health_check_start, 1), $lt: Timestamp(health_check_end, 1) } }] }, { $set: { host: hostname, ts: ts } }, { multi: true });

// add host to db_stats docs
db.db_stats.update({$and: [{ host: { $exists: false } }, { operationTime: { $gte: Timestamp(health_check_start, 1), $lt: Timestamp(health_check_end, 1) } }] }, { $set: { host: hostname, ts: ts } }, { multi: true })

//add frag info to coll_stats
{
    mongodb_rs_frag.forEach(fragInfo => {
        ns = fragInfo.db + '.' + fragInfo.collection;
        db.coll_stats.update({ $and: [{ fragInfo: { $exists: false } }, { ns: ns }, { host: hostname }] }, { $set: { fragInfo: fragInfo } }, { multi: true });
    });
}