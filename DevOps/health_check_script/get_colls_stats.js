// get all collections stats //

if(version < 8){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

var alldbs = db.getMongo().getDBNames();

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);
    db.getCollectionNames().forEach((c) => {
        printjson(db.runCommand({
            collStats: c
    }));})
}