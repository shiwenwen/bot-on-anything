# app.py
from flask import Flask, request, render_template, make_response, jsonify
import multiprocessing
from datetime import timedelta
from app import main
from common import log
import json
import argparse
import os


os.environ['TZ'] = 'Asia/Shanghai'
http_app = Flask(__name__, static_url_path='')
# 自动重载模板文件
http_app.jinja_env.auto_reload = True
http_app.config['TEMPLATES_AUTO_RELOAD'] = True
# 设置静态文件缓存过期时间
http_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 微信二维码链接
qrcode_link = None


@http_app.route('/', methods=['GET'])
def index():
    log.info('访问首页')
    return render_template('index.html')


bot_process: multiprocessing.Process = None


@http_app.route('/api/restart', methods=['POST'])
def restart():
    global bot_process
    if bot_process and bot_process.is_alive():
        bot_process.terminate()
    # 创建子进程对象
    bot_process = multiprocessing.Process(target=main)
    json_data = request.get_json()
    re_login = json_data.get('re_login', False)
    if re_login:
        # 删除itchat的缓存文件
        os.remove('itchat.pkl')
    # 启动进程
    bot_process.start()
    return jsonify({
        'code': 0,
        'msg': 'restart success'
    })


@http_app.route('/api/save_config', methods=['POST'])
def sava_config():
    json_data = request.get_json()
    # 读取本地的config.json文件
    with open('config.json', 'r') as f:
        config = json.load(f)
        # 修改配置
        new_config = _merge_dict(config, json_data, {'group_character_desc': True})
        # 写入本地的config.json文件
        with open('config.json', 'w') as f:
            json.dump(new_config, f, indent=3, ensure_ascii=False)
        return jsonify({
            'code': 0,
            'msg': 'save success'
        })


@http_app.route('/api/config', methods=['GET'])
def get_config():
    # 读取本地的config.json文件
    with open('config.json', 'r') as f:
        config = json.load(f)
        return jsonify({
            'code': 0,
            'msg': 'success',
            'data': config
        })


@http_app.route('/api/receive_qrcode', methods=['POST'])
def receive_qrcode():
    json_data = request.get_json()
    global qrcode_link
    qrcode_link = json_data.get('qrcode_link')
    log.info('收到二维码 %s' % qrcode_link)
    return jsonify({
        'code': 0,
        'msg': 'success'
    })


@http_app.route('/api/query_qrcode', methods=['GET'])
def query_qrcode():
    global qrcode_link
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': {
            'qrcode_link': qrcode_link
        }
    })


def _merge_dict(a:dict, b:dict, ignore_dict:dict):
    for k, v in b.items():
        if isinstance(v, dict) and not ignore_dict.get(k, False):
            a[k] = _merge_dict(a.get(k, {}), v, ignore_dict)
        else:
            a[k] = v
    return a


if __name__ == '__main__':
    # 获取启动参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", type=bool, default=True, help="debug模式")
    parser.add_argument("--host", type=str, default='0.0.0.0', help="host")
    parser.add_argument("--port", type=int, default=5000, help="port")
    args = parser.parse_args()
    http_app.run(debug=args.debug, host=args.host, port=args.port)

