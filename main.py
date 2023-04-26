# app.py
from flask import Flask, request, render_template, make_response, jsonify
import multiprocessing
from datetime import timedelta
from app import main

http_app = Flask(__name__, static_url_path='')
# 自动重载模板文件
http_app.jinja_env.auto_reload = True
http_app.config['TEMPLATES_AUTO_RELOAD'] = True
# 设置静态文件缓存过期时间
http_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@http_app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# bot_process: multiprocessing.Process = None
# @http_app.route('/', methods=['GET'])
# def save():
#     global bot_process
#     if bot_process and bot_process.is_alive():
#         bot_process.terminate()
#         bot_process = None
#         return jsonify({
#             'code': 0,
#             'msg': 'shutdown success'
#         })
#     else:
#         # 创建子进程对象
#         bot_process = multiprocessing.Process(target=main)
#         # 启动进程
#         bot_process.start()
#         return jsonify({
#             'code': 0,
#             'msg': 'start success'
#         })


if __name__ == '__main__':
    http_app.run(debug=True)
