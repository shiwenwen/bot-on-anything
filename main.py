# app.py
from flask import Flask, request, render_template, make_response, jsonify
import multiprocessing
from datetime import timedelta
from app import main
from common import log
import json


http_app = Flask(__name__, static_url_path='')
# 自动重载模板文件
http_app.jinja_env.auto_reload = True
http_app.config['TEMPLATES_AUTO_RELOAD'] = True
# 设置静态文件缓存过期时间
http_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 微信二维码链接
wechat_qrcode_link = None


@http_app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


bot_process: multiprocessing.Process = None
@http_app.route('/restart', methods=['GET'])
def save():
    global bot_process
    if bot_process and bot_process.is_alive():
        bot_process.terminate()
        # 创建子进程对象
        bot_process = multiprocessing.Process(target=main)
        # 启动进程
        bot_process.start()
        return jsonify({
            'code': 0,
            'msg': 'restart success'
        })


@http_app.route('/config', methods=['POST'])
def sava_config():
    json_data = request.get_json()
    # 读取本地的confifig.json文件
    with open('config.json', 'r') as f:
        config = json.load(f)
        # 修改配置
        new_config = _merge_dict(config, json_data)
        # 写入本地的config.json文件
        with open('config.json', 'w') as f:
            json.dump(json_data, f)
        return jsonify({
            'code': 0,
            'msg': 'save success'
        })



@http_app.route('/receive_qrcode', methods=['POST'])
def receive_qrcode():
    json_data = request.get_json()
    global wechat_qrcode_link
    wechat_qrcode_link = json_data.get('qrcode_link')
    return jsonify({
        'code': 0,
        'msg': 'success'
    })


@http_app.route('/query_qrcode', methods=['GET'])
def query_qrcode():
    global wechat_qrcode_link
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': {
            'qrcode_link': wechat_qrcode_link
        }
    })


def _merge_dict(a, b):
    for k, v in b.items():
        if isinstance(v, dict):
            a[k] = _merge_dict(a.get(k, {}), v)
        else:
            a[k] = v
    return a



if __name__ == '__main__':
    http_app.run(debug=True, host='0.0.0.0', port=5000)
