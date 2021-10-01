// get replica set member lag time //

if(version < 2){
    db.printSlaveReplicationInfo();
}else{
    db.printSecondaryReplicationInfo();
}

