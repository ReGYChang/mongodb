var db = db.getSiblingDB(company);
var ts = (new Date()).getTime();

var document = {
    "set" : mongodb_set,
    "serverStatusUptime" : serverStatus_uptime,
    "serverStatusAssertsWarning" : serverStatus_asserts_warning,
    "serverStatusAssertsUser" : serverStatus_asserts_user,
    "serverStatusConnectionCurrent" : serverStatus_connection_current,
    "serverStatusConnectionsAvailable" : serverStatus_connections_available,
    "serverStatusPageFaults" : serverStatus_extra_info_page_faults,
    "serverStatusOpLatenciesReadsLatency" : serverStatus_opLatencies_reads_latency,
    "serverStatusOpLatenciesReadsOps" : serverStatus_opLatencies_reads_ops,
    "serverStatusOpLatenciesWritesLatency" : serverStatus_opLatencies_writes_latency,
    "serverStatusOpLatenciesWritesOps" : serverStatus_opLatencies_writes_ops,
    "serverStatusCursorTimedOut" : serverStatus_cursor_timedOut,
    "serverStatusOperationScanAndOrder" : serverStatus_operation_scanAndOrder,
    "serverStatusOperationWriteConflicts" : serverStatus_operation_writeConflicts,
    "ts" : ts
}

db.server_status.insert(document);