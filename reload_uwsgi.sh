#!/bin/sh

pids=`lsof | grep '\*\:8088' | awk '{print $2}'` 

for pid in $pids 
do
     echo $pid
     kill $pid
done

sleep 1

uwsgi -x django.xml
