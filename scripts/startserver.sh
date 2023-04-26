#!/bin/bash

#后台启动 main.py
cd `dirname $0`/..
export BASE_DIR=`pwd`
echo $BASE_DIR

# check the nohup.out log output file
#if [ ! -f "${BASE_DIR}/logs/log_info.log" ]; then
#  mkdir "${BASE_DIR}/logs"
#  touch "${BASE_DIR}/logs/log_info.log"
#echo "${BASE_DIR}/logs/log_info.log"
#fi

source ${BASE_DIR}/venv/bin/activate

#nohup python3 "${BASE_DIR}/main.py" --debug=False >> ${BASE_DIR}/logs/log_info.log 2>&1 &
nohup python3 "${BASE_DIR}/main.py" --debug=False >> /dev/null 2>&1 &
echo "bot-on-anaything http server is starting"