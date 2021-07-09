var insert_test = function (n) {
    var time = (new Date()).getTime();
    db.ha_test.insert({ "name": "HA", "ns": i, "ts": time });
}

for (var i = 1; i <= 100000; i++ ) {
    insert_test(i);
}