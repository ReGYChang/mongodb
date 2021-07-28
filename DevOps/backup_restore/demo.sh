#
# This file is used by cron to Backup the data of oplog collection,the collection is part of local DB.
# The oplog (operations log) is a special capped collection that keeps a rolling record of all operations 
# that modify the data stored in your databases.All replica set members contain a copy of the oplog, 
# in the local.oplog.rs collection, which allows them to maintain the current state of the database.
# Each operation in the oplog is idempotent. That is, oplog operations produce the same results 
# whether applied once or multiple times to the target dataset.
#
# We backup the collections by periodicity to restore the DB  in case of  DB disaster 
# The version is defined V.001
# Version   ModifyTime                ModifyBy              Desc
# Ver001    2018-11-06 17:00         xuchangpei             Create the Scripts File
#
#
#!/bin/bash

#### 請在此處輸入關鍵引數，例如程式路徑，賬號，密碼，例項埠###
command_linebin="/data/mongodb/mongobin344/bin/mongo"
username="使用者名稱"
password="使用者命名"
port="mongo都被的埠號"
####
####comments0 start 第一次執行此指令碼時，自動檢查建立備份路徑 ####
if [ ! -d "/data/mongodb_back/mongodboplog_back/mongo$port" ]
then
  mkdir -p /data/mongodb_back/mongodboplog_back/mongo$port
fi

if [ ! -d "/data/mongodb_back/mongodboplog_back/log/$port" ]
then
  mkdir -p /data/mongodb_back/mongodboplog_back/log/$port
fi

bkdatapath=/data/mongodb_back/mongodboplog_back/mongo$port
bklogpath=/data/mongodb_back/mongodboplog_back/log/$port

####comments end ##

logfilename=$(date -d today +"%Y%m%d")

echo "===================================Message --=MongoDB 埠為" $port "的差異備份開始，開始時間為" $(date -d today +"%Y%m%d%H%M%S") >> $bklogpath/$logfilename.log

ParamBakEndDate=$(date +%s)
echo "Message --本次備份時間引數中的結束時間為：" $ParamBakEndDate >> $bklogpath/$logfilename.log

DiffTime=$(expr 65 \* 60)

echo "Message --備份設定的間隔時間為：" $DiffTime >> $bklogpath/$logfilename.log


ParamBakStartDate=$(expr $ParamBakEndDate - $DiffTime)
echo "Message --本次備份時間引數中的開始時間為：" $ParamBakStartDate >> $bklogpath/$logfilename.log

bkfilename=$(date -d today +"%Y%m%d%H%M%S")

#### comments1 start 獲取資料庫中oplog記錄的開始範圍，防止匯出的資料不完整 ####

command_line="${command_linebin} localhost:$port/admin -u$username -p$password"

opmes=$(/bin/echo "db.printReplicationInfo()" | $command_line --quiet)

echo $opmes > opdoctime$port.tmplog

opbktmplogfile=opdoctime$port.tmplog

#opstartmes=$(grep "oplog first event time" $opmes)

opstartmes=$(grep "oplog first event time" $opbktmplogfile | awk -F 'CST' '{print $1}' | awk -F 'oplog first event time: '  '{print $2}' | awk -F ' GMT' '{print $1}'  )

echo "Message --oplog集合記錄的開始時間為："$opstartmes >> $bklogpath/$logfilename.log

oplogRecordFirst=$(date -d "$opstartmes"  +%s)

echo "Message --oplog集合記錄的開始時間為:" $oplogRecordFirst >> $bklogpath/$logfilename.log

##begin 比較備份引數的開始時間是否在oplog記錄的時間範圍內
if [ $oplogRecordFirst -le $ParamBakStartDate ]
then
echo "Message --檢查設定備份時間合理。備份引數的開始時間在oplog記錄的時間範圍內。" >> $bklogpath/$logfilename.log
else echo "Fatal Error --檢查設定的備份時間不合理合理。備份引數的開始時間不在oplog記錄的時間範圍內。請調整oplog size或調整備份頻率。本次備份可以持續進行，但還原時資料完整性丟失。" >> $bklogpath/$logfilename.log
fi

##end##

#### comments1 end  ####

dumpmsg=$(/data/mongodb/mongobin344/bin/mongodump -h localhost --port $port --authenticationDatabase admin -u$username -p$password -d local -c oplog.rs  --query '{ts:{$gte:Timestamp('$ParamBakStartDate',1),$lte:Timestamp('$ParamBakEndDate',9999)}}' -o $bkdatapath/mongodboplog$   )

echo "本次匯出的具體資訊如下：" $dumpmsg
echo $dumpmsg >> $bklogpath/$logfilename.log

#### comments2 start  再次檢查，防止匯出oplog資料過程耗時過長，比如，我們一小時匯出一份，每一次迴圈涵蓋65分鐘，如果匯出執行過程耗時5分鐘以上就可能導致匯出的資料不完整。####
## 下面的70 是有上面的65+5而得，+5 是允許匯出耗時5分鐘。這個邏輯有點繞，大家可以測測，這段邏輯看幾分鐘可以理解通透了。
DiffTime=$(expr 70 \* 60)
AllowMaxDate=$(expr $(date +%s) - $DiffTime)
if [ $AllowMaxDate -le $ParamBakStartDate ]
then
echo "Message --oplog記錄匯出時間在規定的DiffTime範圍內。資料有效" >> $bklogpath/$logfilename.log
else echo "Fatal Error --oplog記錄匯出時間 超出了 規定的DiffTime範圍。資料完整性等不到保證。請增大DiffTime引數或調整備份頻率。" >> $bklogpath/$logfilename.log
fi

#### comments2 end ####

#### comments3 檢查備份檔案是否已經刪除start ####
if [ -d "$bkdatapath/mongodboplog$bkfilename" ]
then
  echo "Message --檢查此次備份檔案已經產生.檔案資訊為:" $bkdatapath/mongodboplog$bkfilename >> $bklogpath/$logfilename.log
  else echo "Fatal Error --備份過程已執行，但是未檢測到備份產生的檔案，請檢查！" >> $bklogpath/$logfilename.log
fi
##### comments3 end ####

#### comments4 start 刪除歷史備份檔案，保留3天，如需調整，請在持續設定
keepbaktime=$(date -d '-3 days' "+%Y%m%d%H")*
if [ -d $bkdatapath/mongodboplog$keepbaktime ]
then
  rm -rf $bkdatapath/mongodboplog$keepbaktime
  echo "Message -- $bkdatapath/mongodboplog$keepbaktime 刪除完畢" >> $bklogpath/$logfilename.log
fi
### comments4 end 


echo "============================Message --MongoDB 埠為" $port "的差異備份結束，結束時間為：" $(date -d today +"%Y%m%d%H%M%S") >> $bklogpath/$logfilename.log