// get all dbs stats //

if(version <= 8){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

var alldbs = db.getMongo().getDBNames();

for(var j = 0; j < alldbs.length; j++){
    var db = db.getSiblingDB(alldbs[j]);
    printjson(db.stats());
}