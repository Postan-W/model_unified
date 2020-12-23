# -*- coding: utf-8 -*-
import json
import logging
import os
import shutil
from zipfile import ZipFile

import requests

_author_ = 'luwt'
_date_ = '2020/1/10 17:06'


logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
DL_DIR_PREFIX = "model/model"
DL_NEED_DIR_PREFIX = ""


def uncompress(zip_path, unzip_path):
    with ZipFile(zip_path, 'r')as f:
        # 深度学习
        zips = list(filter(lambda x: x.startswith(DL_DIR_PREFIX), f.namelist()))
        print(f"zips => {zips}")
        f.extractall(unzip_path, members=zips)
        for src in zips:
            full_src = os.path.join(unzip_path, src)
            dst = full_src.replace(DL_DIR_PREFIX, DL_NEED_DIR_PREFIX)
            print(f"full_src => {full_src}, dst => {dst}")
            dst_parent = os.path.split(dst)[0]
            if not os.path.exists(dst_parent):
                os.mkdir(dst_parent)
            shutil.move(full_src, dst)
        shutil.rmtree(os.path.join(unzip_path, 'model'))


def save_model(local_path, content):
    """
    保存模型文件（zip压缩包）
    :param local_path:
    :param content:
    :return:
    """
    with open(local_path, 'wb')as f:
        f.write(content)


def download_model(local_path, unzip_path):
    """
    调用远程接口下载模型
    :param local_path: 模型下载后的本地保存路径，
        linux设置在根目录下 /model.zip，下载内容为zip压缩包
    :param unzip_path: 解压路径，默认解压到根目录下，即与local_path同级目录
    """
    url = os.environ.get('XQUERY_ADDR') + '/dsModel/downloadModelForModelService'
    # 本地测试url：http://192.168.18.1:8811/datasience/xquery/dsModel/downloadModelForModelService
    params = {
        "modelId": os.environ.get('MODEL_ID'),
        "version": os.environ.get('MODEL_VERSION'),
        "guid": os.environ.get('GUID')
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        logging.info(
            f"请求下载模型接口成功：url => {url}，\n参数为：=> "
            f"{json.dumps(params, indent=4, ensure_ascii=False)}"
        )
        save_model(local_path, res.content)
        # 默认取下载的zip包的同级目录作为解压目录
        uncompress(local_path, unzip_path)
        logging.info("模型下载成功")
        os.remove(local_path)
    else:
        logging.error(f"下载模型失败，reason is => {res.text}")
        raise requests.HTTPError("下载模型失败")


download_model('/root/model.zip', '/models/' + os.environ.get('MODEL_NAME') + '/0001/')

