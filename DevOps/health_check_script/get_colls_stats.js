// get all collections stats //

if(version < 2){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

var alldbs = db.getMongo().getDBNames();

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);

    print("\n\n================================== DB: " + db.getName() + " ==================================")

    db.getCollectionNames().forEach((c) => {
        print("\n\n====================Collection: " + c)
        printjson(db.runCommand({
            collStats: c
    }));})
}