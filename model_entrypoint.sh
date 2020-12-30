#!/bin/bash
string=$HOSTS
array=${string//,/ }
for var in ${array[@]};do echo ${var//<->/ } >> /etc/hosts ; done

python /root/model-server/download_model.py

#nohup tensorflow_model_server --rest_api_port=8505 --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME} "$@" & > /root/tfserver.log

gunicorn -w 1 -b 0.0.0.0:8501 flask_service:app  --chdir /root/model-server