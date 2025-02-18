#!/bin/bash
#后台运行bot-on-anaything执行脚本

cd `dirname $0`/..
export BASE_DIR=`pwd`
echo $BASE_DIR

# check the nohup.out log output file
if [ ! -f "${BASE_DIR}/logs/log_info.log" ]; then
  mkdir "${BASE_DIR}/logs"
  touch "${BASE_DIR}/logs/log_info.log"
echo "${BASE_DIR}/logs/log_info.log"
fi

# source ${BASE_DIR}/venv/bin/activate

nohup python3 "${BASE_DIR}/app.py" >> /dev/null 2>&1 &


echo "bot-on-anaything is starting"

