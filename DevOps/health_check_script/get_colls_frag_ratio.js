// get all collections space fragmentation ratio //

if(version.split('.')[2] < 8){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

function getCollectionDiskSpaceFragRatio(dbname, coll) {
    var fragInfo = new Object();
    var res = db.getSiblingDB(dbname).runCommand({
        collStats: coll
    });
    var totalStorageUnusedSize = 0;
    var totalStorageSize = res['storageSize'] + res['totalIndexSize'];
    Object.keys(res.indexDetails).forEach(function(key) {
        var size = res['indexDetails'][key]['block-manager']['file bytes available for reuse'];
        totalStorageUnusedSize += size;
    });
    var size = res['wiredTiger']['block-manager']['file bytes available for reuse'];
    totalStorageUnusedSize += size;

    fragInfo.db = dbname;
    fragInfo.collection = coll;
    fragInfo.totalStorageUnusedSize = totalStorageUnusedSize;
    fragInfo.totalStorageSize = totalStorageSize;
    fragInfo.fragRatio = ((totalStorageUnusedSize * 100.0) / totalStorageSize).toFixed(2) + "%";
    
    return fragInfo;
}

var alldbs = db.getMongo().getDBNames();
var fragInfos = [];

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);
    db.getCollectionNames().forEach((c) => {fragInfos.push(getCollectionDiskSpaceFragRatio(db.getName(), c));});
}

print(JSON.stringify(fragInfos));