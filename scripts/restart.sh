# 获取当前脚本所在目录的路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# 执行shutdown.sh脚本
sh ${SCRIPT_DIR}/shutdown.sh
echo "服务已关闭"
# 执行start.sh脚本
echo "服务开始启动"
sh ${SCRIPT_DIR}/start.sh
