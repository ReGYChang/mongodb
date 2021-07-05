var insert_test = function (n) {
    var time = (new Date()).getTime();
    db.backup_test.insert({ "name": "backup", "ns": i, "ts": time });
}

for (var i = 100001; i <= 150000; i++ ) {
    insert_test(i);
}