import json

import numpy as np
import torch
from PIL import Image
from pypmml import Model

# img = Image.open("123.jpg")
# print(np.asarray(img))
# print(np.resize(img,[1,1]))
# print(np.resize(img, [1, 28, 28, 1]))

# data = {
#     "packname": "gol",
#     "app_version": "123",
#     "netmodel": "123",
#     "geohash_2": "123",
#     "geohash_4": "123",
#     "geohash_5": "123",
#     "sim_pos_5_minutes": 1,
#     "sim_neg_5_minutes": 1,
#     "sim_pos_60_minutes": 1,
#     "sim_neg_60_minutes": 1,
#     "sim_pos_360_minutes": 1,
#     "sim_neg_360_minutes": 1,
#     "sim_pos_3month": 1,
#     "news_inview": 1,
#     "news_click": 1,
#     "page_no": 1,
#     "tagSim_5min": 1,
#     "tagSim_60min": 1,
#     "tagSim_360min": 1,
#     "tagSim_3month": 1,
#     "ctr_2day": 1,
#     "ctr_1week": 1,
#     "ctr_3month": 1
# }
#
# model = Model.load("./models/lightgbm_video_20200531.pmml")
# result = model.predict(data).toString()
# print(type(result))
# print(result)
#
# model.close()


# print(json.dumps({"gollong  loveeeeeeeee":123}))

# print(json.loads('{"gollong  loveeeeeeeee": 123}'))

# import saved_model_tool
#
# print(saved_model_tool.show_all("./models/model"))
#
# {'test_signature': {'inputs': '{\'input_xv\': name: "feat_value:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n  dim {\n    size: -1\n  }\n}\n, '
#                               '\'input_xi\': name: "feat_index:0"\ndtype: DT_INT32\ntensor_shape {\n  dim {\n    size: -1\n  }\n  dim {\n    size: -1\n  }\n}\n, '
#                               '\'dropout_keep_deep\': name: "dropout_deep_deep:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n}\n, '
#                               '\'dropout_keep_fm\': name: "dropout_keep_fm:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n}\n}',
#
#
#                     'outputs': '{\'outputs\': name: "Sigmoid:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n  dim {\n    size: 1\n  }\n}\n}'}}


# model = torch.load('src/model.pth')  # 直接加载模型

# import os
# if not (os.environ.get('MODEL_NAME') and os.environ.get('XQUERY_ADDR') and os.environ.get(
#         'MODEL_SERVICE_ID') and os.environ.get('API_ADDR') and os.environ.get('MODEL_TYPE')):
#     print("缺少环境变量")
#     raise Exception("缺少环境变量")
#
#
# import saved_model_tool
#
# import tensorflow as tf
# import numpy as np
#
# print(saved_model_tool.show_all("./models/saved_models"))
#
#
#
# model = tf.keras.experimental.load_from_saved_model("./models/saved_models")
# # model = tf.keras.models.load_model("./models/saved_models")
#
# data = {"dense_6_input":np.random.randint(0,255,(1,784))}
# print(model.predict(data))
#
# # {'__saved_model_init_op':
# #      {'inputs': '{}', 'outputs': '{\'__saved_model_init_op\': name: "init_1"\ntensor_shape {\n  unknown_rank: true\n}\n}'},
# #  'serving_default':
# #      {'inputs': '{\'dense_6_input\': name: "dense_6_input:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n  dim {\n    size: 784\n  }\n}\n}',
# #       'outputs': '{\'dense_7\': name: "dense_7/Softmax:0"\ndtype: DT_FLOAT\ntensor_shape {\n  dim {\n    size: -1\n  }\n  dim {\n    size: 10\n  }\n}\n}'}}


import os
# print(os.path.splitext("/models/model/aaa.onnx"))
# print(os.path.splitext("/models/model/aaa.pb"))
# print(os.path.splitext("/models/model"))
#
#
# print("/models/model".split(".")[-1])
# print("/models/model/aaa.pb".split(".")[-1])
# print("/models/model/aaa.onnx".split(".")[-1])

# print(os.environ.get('MODEL_NAME'))


import torchvision as tv
import torchvision.transforms as transforms
import torch as t
from PIL import Image


device = t.device("cpu" if t.cuda.is_available() else "cpu")
# model = tv.models.resnet18(pretrained=True)  # 创建一个模型
model = t.load('models/model.pth')
model = model.to(device)
# t.save(model, 'models/model.pth')
# model = t.load('src/model.pth')  # 直接加载模型
model.eval()  # 预测模式

# 获取测试图片，并行相应的处理
img = Image.open('123.jpg')
transform = transforms.Compose([transforms.Resize(256),  # 重置图像分辨率
                                transforms.CenterCrop(224),  # 中心裁剪
                                transforms.ToTensor(), ])
img = img.convert("RGB")  # 如果是标准的RGB格式，则可以不加
img = transform(img)
img = img.unsqueeze(0)
img = img.to(device)

# print(img)

with t.no_grad():
    py = model(img)

    print(list(model.parameters()))
    print(model.get_inputs())
    print(py.tolist())
# _, predicted = t.max(py, 1)  # 获取分类结果
# classIndex_ = predicted[0]

# print('预测结果', classIndex_)
