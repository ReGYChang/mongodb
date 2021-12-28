// get replica set member lag time //

if(version.split('.')[2] < 8){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

