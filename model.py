import abc
import base64
import io
import onnxruntime
import requests
import tensorflow as tf
from pypmml import Model

from utils import analysis_list
import saved_model_tool
import numpy as np
import operator
from PIL import Image
import logging
import json

"""
抽象的模型类，需要实现为以下几个模型格式：savedmodel、onnx、pmml、h5、ckpt、pb
"""

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}


class AbstractModel(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def predict(self, data):
        pass

    @abc.abstractmethod
    def get_info(self):
        pass


class PMMLModel(AbstractModel):

    def __init__(self, model_name, model_inputs):
        self.inputs = model_inputs

        self.model = Model.load(model_name)
        self.inputFields = self.model.inputFields
        self.inputNames = self.model.inputNames
        self.outputFields = self.model.outputFields
        self.outputNames = self.model.outputNames
        self.info = {"inputs": self.outputNames, "outputs": self.outputNames}
        logging.info("模型基本信息:::")
        logging.info(self.info)

    def __del__(self):
        if self.model:
            self.model.close()

    def get_info(self):
        return self.info

    def predict(self, data):
        return self.model.predict(data).toString()


class H5Model(AbstractModel):

    def __init__(self, model_name, model_inputs):
        self.inputs = json.loads(model_inputs)

        self.model = tf.keras.models.load_model(model_name)
        self.info = None
        # TODO 暂时无法获取
        logging.info("模型基本信息:::")
        logging.info(self.info)

        self.model.summary()

    def get_info(self):
        return self.info

    def predict(self, data):
        for k, v in data.items():

            # input_data[item] = np.asarray(input_data[item], dtype=np.float32)
            if v["type"] == "image":
                base64_img = base64.urlsafe_b64decode(v["data"])
                image = io.BytesIO(base64_img)
                img = Image.open(image)
                data[k] = np.resize(img, self.inputs[k]["shape"])

            elif v["type"] == "url":
                response = requests.get(v["data"], headers=headers)
                image = io.BytesIO(response.content)
                img = Image.open(image)
                data[k] = np.resize(img, self.inputs[k]["shape"])

            elif v["type"] == "common":
                if not operator.eq(list(np.array(v["data"]).shape), self.inputs[k]["shape"]):
                    raise Exception("形状异常")
                data[k] = v["data"]

        result = self.model.predict(data).tolist()
        return result


class SMModel(AbstractModel):

    def __init__(self, model_name, model_inputs):
        self.inputs = json.loads(model_inputs)

        self.model = tf.keras.experimental.load_from_saved_model(model_name)
        # self.inputs_info, \
        # self.outputs_info, \
        # self.inputs, \
        # self.inputs_shape, \
        # self.outputs = \
        #     saved_model_tool.show_all(model_name)

        self.info = saved_model_tool.show_all(model_name)
        logging.info("模型基本信息:::")
        logging.info(self.info)

    def get_info(self):
        return self.info

    def predict(self, data):
        for k, v in data.items():

            if v["type"] == "image":
                base64_img = base64.urlsafe_b64decode(v["data"])
                image = io.BytesIO(base64_img)
                img = Image.open(image)
                # data[k] = np.asarray(np.resize(img, v["shape"]))
                # 4维度resize成2维度现在会出现问题，需要先resize4维度再reshape2维度
                data[k] = np.resize(img, self.inputs[k]["shape"])

            elif v["type"] == "url":
                response = requests.get(v["data"], headers=headers)
                image = io.BytesIO(response.content)
                img = Image.open(image)
                data[k] = np.resize(img, self.inputs[k]["shape"])

            elif v["type"] == "common":
                if not operator.eq(list(np.array(v["data"]).shape), self.inputs[k]["shape"]):
                    raise Exception("形状异常")
                data[k] = v["data"]

        result = self.model.predict(data).tolist()

        return result


class ONNXModel(AbstractModel):

    def __init__(self, model_name, model_inputs):
        self.inputs = json.loads(model_inputs)

        self.sess = onnxruntime.InferenceSession(model_name)
        self.inputs_info = self.get_inputs()
        self.outputs_info = self.get_outputs()
        self.inputs_local = analysis_list(self.inputs_info)
        self.output_list = analysis_list(self.outputs_info)

        self.metadatas = self.get_modelmeta()
        self.info = {"inputs": self.inputs_info, "outputs": self.outputs_info, "custom_metadata_map": self.metadatas[0],
                     "description": self.metadatas[1], "domain": self.metadatas[2], "graph_name": self.metadatas[3],
                     "producer_name": self.metadatas[4], "version": self.metadatas[5]}
        logging.info("模型基本信息:::")
        logging.info(self.info)

    def predict(self, data):
        predict_data = {}
        #     data = {
        #         "input_1": {"data":img,"type":"images","shape":[1,3,224,224]},
        #         "image_shape": {"data":[[1,2]],"type":"common","shape":[1,2]}
        #     }

        for k, v in data.items():
            # input_data[item] = np.asarray(input_data[item], dtype=np.float32)
            if v["type"] == "image":
                base64_img = base64.urlsafe_b64decode(v["data"])
                image = io.BytesIO(base64_img)
                img = Image.open(image)
                data[k] = np.resize(img, self.inputs[k]["shape"]).tolist()

            elif v["type"] == "url":
                response = requests.get(v["data"], headers=headers)
                image = io.BytesIO(response.content)
                img = Image.open(image)
                data[k] = np.resize(img, self.inputs[k]["shape"]).tolist()

            elif v["type"] == "common":
                if not operator.eq(list(np.array(v["data"]).shape), self.inputs[k]["shape"]):
                    raise Exception("形状异常")
                data[k] = v["data"]
        result = self.sess.run(self.output_list, data)
        return [item.tolist() for item in result]

    def get_info(self):
        return self.info

    def get_inputs(self) -> []:
        # input_name = sess.get_inputs()[0].name
        # input_shape = sess.get_inputs()[0].shape
        # input_type = sess.get_inputs()[0].type
        input_info = [{model_input.name: {'shape': model_input.shape, 'type': model_input.type}} for model_input in
                      self.sess.get_inputs()]
        return input_info

    def get_outputs(self) -> []:
        # output_name = sess.get_outputs()[0].name
        # output_shape = sess.get_outputs()[0].shape
        # output_type = sess.get_outputs()[0].type
        input_info = [{model_output.name: {'shape': model_output.shape, 'type': model_output.type}} for model_output in
                      self.sess.get_outputs()]
        return input_info

    def get_modelmeta(self):
        custom_metadata_map = self.sess.get_modelmeta().custom_metadata_map
        description = self.sess.get_modelmeta().description
        domain = self.sess.get_modelmeta().domain
        graph_name = self.sess.get_modelmeta().graph_name
        producer_name = self.sess.get_modelmeta().producer_name
        version = self.sess.get_modelmeta().version
        return custom_metadata_map, description, domain, graph_name, producer_name, version


if __name__ == '__main__':
    # onnx = ONNXModel('mobilenetv2-7.onnx')
    # print(onnx.info)
    # img = Image.open('123.jpg')
    #
    #
    # # tiny-yolov3-11.onnx
    # data1 = {
    #     "input_1": {"data":img,"type":"image","shape":[1,3,224,224]},
    #     "image_shape": {"data":[[1,2]],"type":"common","shape":[1,2]}
    # }
    # # mobilenetv2-7.onnx
    # data2 = {
    #     "data": {"data":img,"type":"image","shape":[1,3,224,224]},
    # }
    #
    # predict_result = onnx.predict(data2)
    # print(predict_result)

    # pmml = PMMLModel("lightgbm_video_20200531.pmml")
    # print(str(pmml.inputFields[0]))
    # print(pmml.inputNames)
    # print(pmml.outputFields)
    # print(pmml.outputNames)
    # data = {
    #     "packname": "gol", "app_version": "123", "netmodel": "123",
    #     "geohash_2": "123", "geohash_4": "123", "geohash_5": "123",
    #     "sim_pos_5_minutes": 1, "sim_neg_5_minutes": 1, "sim_pos_60_minutes": 1,
    #     "sim_neg_60_minutes": 1, "sim_pos_360_minutes": 1, "sim_neg_360_minutes": 1,
    #     "sim_pos_3month": 1, "news_inview": 1, "news_click": 1,
    #     "page_no": 1, "tagSim_5min": 1, "tagSim_60min": 1,
    #     "tagSim_360min": 1, "tagSim_3month": 1, "ctr_2day": 1,
    #     "ctr_1week": 1, "ctr_3month": 1
    # }
    # print(pmml.predict(data))

    # sm = SMModel("./saved_models")
    #
    # data3 = {
    #     "dense_6_input": {"data": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1600161420065&di=0a5582cf971f0897d80cb8aa411df44d&imgtype=0&src=http%3A%2F%2Fpic1.win4000.com%2Fpic%2F1%2F44%2F5ca4594503.jpg_195.jpg", "type": "url", "shape": [1, 784]},
    # }
    # print(sm.predict(data3))

    # h5 = H5Model("123")
    # rand = np.random.randint(0,255,(2,784))
    # print(h5.predict(rand))
    pass
