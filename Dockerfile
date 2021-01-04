FROM 1135085247/wmingzhu:v2
#1135085247/wmingzhu:v2基础镜像包含了centos8,python3.6.8环境，conda环境，配置好国内源的pip,tensorflow-gpu==2.2.0,

#run的时候加上/bin/bash
#SHELL["/bin/bash","-c"]

USER root

LABEL "date"="2020-12"
LABEL "register"="root" \
"password"="l8X6%WAqc9ifGX6o" \
"link"="140.210.92.100"

#--build-arg <varname>=<value>
ARG builder=wmingzhu

#ONBUILD RUN ls -al

HEALTHCHECK --interval=30m --timeout=5s CMD curl -f http://localhost:5000/successful || exit 1

COPY model-server /root/model-server/

WORKDIR /root/model-server

ENV MODEL_BASE_PATH=/models

RUN mkdir -p ${MODEL_BASE_PATH}

#应该在docker run的时候明确指定宿主机目录，这里匿名挂载
VOLUME /root/model-server

# gRPC
EXPOSE 8500
# REST
EXPOSE 8501
EXPOSE 5000

RUN ls -l /root/model-server/model_entrypoint.sh
RUN cp /root/model-server/model_entrypoint.sh /usr/bin/model_entrypoint.sh \
    && chmod +x /usr/bin/model_entrypoint.sh

#ENTRYPOINT ["/usr/bin/model_entrypoint.sh"]
