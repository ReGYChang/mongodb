var db = db.getSiblingDB(company);

// add host to coll_stats docs
db.coll_stats.update({operationTime: { $gte: Timestamp(1600000000, 1), $lt: Timestamp(1700000000, 1) }}, { $set: { host: "test3" } }, { multi: true });

// add host to db_stats docs
db.db_stats.update({operationTime: { $gte: Timestamp(1600000000, 1), $lt: Timestamp(1700000000, 1) }}, { $set: { host: "test3" } }, { multi: true });

//add frag info to coll_stats
{mongodb_rs_frag.forEach(fragInfo => {
    ns = fragInfo.db + '.' + fragInfo.collection;
    db.coll_stats.update({ns: ns},{$set:{fragInfo : fragInfo}},{multi : true});
});}