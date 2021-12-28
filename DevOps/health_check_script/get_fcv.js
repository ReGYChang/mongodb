if(version.split('.')[2] < 8){
    db.getMongo().setSlaveOk();
}else{
    rs.secondaryOk();
}

printjson(db.adminCommand( { getParameter: 1, featureCompatibilityVersion: 1 } ));