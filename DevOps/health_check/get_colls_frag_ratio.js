// get all collections space fragmentation ratio //

function getCollectionDiskSpaceFragRatio(dbname, coll) {
    var res = db.getSiblingDB(dbname).runCommand({
        collStats: coll
    });
    var totalStorageUnusedSize = 0;
    var totalStorageSize = res['storageSize'] + res['totalIndexSize'];
    Object.keys(res.indexDetails).forEach(function(key) {
        var size = res['indexDetails'][key]['block-manager']['file bytes available for reuse'];
        print("index table " + key + " unused size: " + size);
        totalStorageUnusedSize += size;
    });
    var size = res['wiredTiger']['block-manager']['file bytes available for reuse'];
    print("collection table " + coll + " unused size: " + size);
    totalStorageUnusedSize += size;
    print("collection and index table total unused size: " + totalStorageUnusedSize);
    print("collection and index table total file size: " + totalStorageSize);
    print("Fragmentation ratio: " + ((totalStorageUnusedSize * 100.0) / totalStorageSize).toFixed(2) + "%");
}

var alldbs = db.getMongo().getDBNames();

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);
    print("\n\n================================== DB: " + db.getName() + " ==================================")
    db.getCollectionNames().forEach((c) => {print("\n\n" + c); getCollectionDiskSpaceFragRatio(db.getName(), c);});
}