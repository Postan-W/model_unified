# -*- coding: utf-8 -*-
import json
import logging
import os
import shutil
from zipfile import ZipFile

import requests

_author_ = 'luwt'
_date_ = '2020/1/10 17:06'
_modified_by = "wmingzhu"
_modified_date = "2020/12-"
_statement_ = "修改了日志记录的相关代码，其它未动"

# logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("./logs/downloadmodellog.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

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
            finalname = full_src.replace(DL_DIR_PREFIX, DL_NEED_DIR_PREFIX)
            print(f"full_src => {full_src}, dst => {finalname}")
            finalname_parent = os.path.split(finalname)[0]
            if not os.path.exists(finalname_parent):
                os.mkdir(finalname_parent)
                #改名
            shutil.move(full_src, finalname)
        #删除上面填入的解压路径，下面的文件也全部删除(当然，上面的移动操作已经将文件移走了)
        shutil.rmtree(unzip_path)


def save_model(local_path, content):
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
            f"请求成功：url =>> {url}，\n参数为：=> "
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

