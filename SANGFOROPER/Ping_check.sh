#!/bin/bash
IP=10.10.10.2
dir="/sangfor/Shscripts/pdc/"
if [ ! -d ${dir} ];then
	mkdir -p ${dir}
fi
echo 1 > ${dir}pdcping.lock
while true
do
	Time=`date +%F`
	TIME="${Time} 23:59"
	if [ "${data}" == "${TIME}" ];then
		mkdir ${dir}${Time} && mv ${dir}pdcping.log ${dir}${Time}-pingpdc.log
		mv ${dir}${Time}-pingpdc.log ${dir}${Time}
	fi
	find ${dir} -mtime +7 -type d -exec rm -rf {} \;

	find ${dir} -mtime +7 -name "*-pingpdc.log" -exec rm -rf {} \;
	data=`date +%F' '%H:%M`
	data1=`date +%F' '%H:%M:%S`
	echo "------------${data1}---------------">>${dir}pingpdc.log
	ping -c 10 ${IP} >>${dir}pingpdc.log
	if [ $? -eq 1 ];then
		STAT=`cat ${dir}pdcping.lock`
		if [ ${STAT} -eq 1 ];then
                        /usr/local/python34/bin/python3 /sangfor/Pysangfor/SangFor_check.py
			echo 0 > ${dir}pdcping.lock
		else
			continue
		fi
	else
		STAT=`cat ${dir}pdcping.lock`
		if [ ${STAT} -eq 0 ];then
			echo 1 > ${dir}pdcping.lock
		else
			continue
		fi
	fi


done

