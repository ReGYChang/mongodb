// get replica set member lag time //

if(version < 8){
    db.printSlaveReplicationInfo();
}else{
    db.printSecondaryReplicationInfo();
}

