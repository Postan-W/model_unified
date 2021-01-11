#!/bin/bash
string=$HOSTS
array=${string//,/ }
for var in ${array[@]};do echo ${var//<->/ } >> /etc/hosts; done
echo enter the container
python /root/model_server/download_model2.py

#nohup tensorflow_model_server --rest_api_port=8505 --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME} "$@" & > /root/tfserver.log

#指定worker数、地址与端口、模块和flask对象、启动目录
gunicorn -w 1 -b 0.0.0.0:5000 flask_service:app  --chdir /root/model_server/

#--config /root/model-server/config.txt