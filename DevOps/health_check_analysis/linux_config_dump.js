var db = db.getSiblingDB(company);
var ts = (new Date()).getTime();

var document = {
  "host" : hostname,
  "quarter" : quarter,
  "cpuModel" : cpu_model,
  "hypervisor" : hypervisor,
  "osVersion" : os_version,
  "memSwap" : mem_swap,
  "homeSpaceTotal" : home_space_total,
  "homeSpaceUsed" : home_space_used,
  "uptime" : uptime,
  "ulimitNproc" : ulimit_nproc,
  "ulimitNofile" : ulimit_nofile,
  "readahead" : readahead,
  "selinux" : isSelinux,
  "thpEnabledFlag" : thp_enabled_flag,
  "thpDefragFlag" : thp_defrag_flag,
  "vmZoneReclaimMode" : vm_zone_reclaim_mode,
  "vmSwappiness" : vm_swappiness,
  "ts" : ts
}

db.linux_config.insert(document);