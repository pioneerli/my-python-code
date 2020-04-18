#!/bin/bash
num=$(ps -ef |grep pdc.sh|wc -l)
cmd="/usr/bin/nohup /bin/bash /sangfor/Shscripts/pdc/Ping_check.sh &"

if [ ${num} -lt 2 ];then
${cmd}
fi

