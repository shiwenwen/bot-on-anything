#!/bin/bash

#关闭服务
#查找端口为5000的进程，如果存在则杀掉，否则提示服务未启动，无需关闭，退出脚本，使用lsof -i:5000命令查看端口占用情况
 pid=`lsof -i:5000 | grep LISTEN | awk '{print $2}'`
 if [ -z "$pid" ] ; then
         echo "No bot-on-anaything server running."
         exit 0;
 fi

 echo "The bot-on-anaything server(${pid}) is running..."

 kill ${pid}

 echo "Send shutdown request to bot-on-anaything server(${pid}) OK"

