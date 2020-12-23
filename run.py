import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import requests
from flask import Flask, jsonify, request
import json
import traceback

from model import SMModel, ONNXModel, H5Model, PMMLModel

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("log", maxBytes=1024 * 1024 * 100, backupCount=10, encoding="UTF-8")
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)

# 获取环境变量
xquery_addr = os.environ.get('XQUERY_ADDR')
model_service_id = os.environ.get('MODEL_SERVICE_ID')
api_addr = os.environ.get('API_ADDR')
model_inputs = os.environ.get('MODEL_INPUTS')
model_outputs = os.environ.get('MODEL_OUTPUTS')
base_path = os.environ.get('MODEL_BASE_PATH')
model_name = os.environ.get('MODEL_NAME')

app.logger.info('MODEL_INPUTS: %s', model_inputs)
app.logger.info('MODEL_OUTPUTS: %s', model_outputs)
app.logger.info('MODEL_NAME: %s', model_name)
app.logger.info('API_ADDR: %s', api_addr)
app.logger.info('MODEL_SERVICE_ID: %s', model_service_id)
app.logger.info('XQUERY_ADDR: %s', xquery_addr)
app.logger.info('MODEL_BASE_PATH: %s', base_path)

if not (model_inputs and model_name and xquery_addr and
        model_service_id and api_addr and model_outputs
        and base_path):
    app.logger.error('缺少环境变量')
    sys.exit(1)


# 验证token
def check_token(token, request_param):
    url = xquery_addr + '/dsModel/serviceApply/tokenVerify'
    app.logger.info('开始校验token，地址为：%s', url)
    body = {
        'callToken': token,
        'serviceId': model_service_id,
        'requestParam': str(request_param)
    }
    headers = {'content-type': 'application/json'}
    app.logger.info('参数为：%s', body)
    response = requests.post(url, data=json.dumps(body), headers=headers)
    return response.text


# 解析模型格式
def analy_model():
    model_path = os.path.join(base_path, model_name)
    assert os.path.exists(model_path), "模型文件不存在，请检查模型文件"

    if os.path.isfile(model_path):
        return model_name.split(".")[-1], model_path

    elif os.path.isdir(model_path):
        return "savedmodel", model_path
    else:
        app.logger.error('无法解析的路径')


model_type, model_path = analy_model()

if model_type == "savedmodel":
    model = SMModel(model_path, model_inputs)
elif model_type == "onnx":
    model = ONNXModel(model_path, model_inputs)
elif model_type == "h5":
    model = H5Model(model_path, model_inputs)
elif model_type == "pmml":
    model = PMMLModel(model_path, model_inputs)
else:
    app.logger.error('不支持当前模型格式:' + model_type)
    sys.exit(1)

app.logger.info("模型加载完毕")


# get:request.args['name']
# formdata:request.form['name']
# file: request.files['file']
# json:request.get_json()


@app.route('/' + api_addr, methods=['POST'])
def route_predict():
    try:
        data = request.get_json()
        token = request.args["token"]
        app.logger.info(token)
        # token_result = check_token(token, '')
        # if json.loads(token_result).get('code', None) != 1000:
        #     return jsonify({'error': 'token认证失败'})
        return jsonify({"result": model.predict(data)})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)})


@app.route('/' + api_addr + '/metadata', methods=['GET'])
def route_metadata():
    try:
        return jsonify(model.get_info())
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8501, debug=False)
