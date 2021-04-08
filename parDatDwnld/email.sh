#!/bin/bash

 network=$1
 station=$2
 timeStamp=`date +%F`
 SENDER="Rover job"
 TITLE="Rover job  ${network}_${station} finished at $timeStamp"
 OUTPUT=$(cd /scratch/tolugboj_lab/Prj10_DeepLrningEq/9_DanielSequencer/3_src/obspy_batch/${network}/${network}-${station}/datarepo && rover list-retrieve ${network}_${station}_*_* 1980-01-01 ${timeStamp} )
 ADDRS=$3
 
cat <<EOF |/usr/sbin/sendmail -t -oi
To: $ADDRS
From: $SENDER
Subject: $TITLE

======================= Rover job update ===============================
network: $1
station: $2
status: finished

missing:
$OUTPUT

========================================================================
EOF



