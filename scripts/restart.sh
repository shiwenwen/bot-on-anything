if [ -f "shutdown.sh" ] && [ -f "start.sh" ]; then
  sh shutdown.sh
  sh start.sh
else
  echo "缺少启动脚本！！！"
fi
