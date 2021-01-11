FROM 1135085247/model_server:v2


SHELL ["/bin/bash","-c"]

#USER root

LABEL "date"="2020-12"
#LABEL "register"="root" \"password"="l8X6%WAqc9ifGX6o" \"link"="140.210.92.100"

#--build-arg <varname>=<value>
ARG builder=wmingzhu

#ONBUILD RUN ls -al

HEALTHCHECK --interval=30m --timeout=5s CMD curl -f http://localhost:5000/successful || exit 1

COPY model_server /root/model_server/

WORKDIR /root/model_server

ENV MODEL_BASE_PATH=/models/

RUN mkdir -p ${MODEL_BASE_PATH}

#应该在docker run的时候明确指定宿主机目录，这里匿名挂载
VOLUME /root/model_server

# gRPC
EXPOSE 8500
# REST
EXPOSE 8501
EXPOSE 5000

RUN ls -l /root/model_server/model_entrypoint.sh
RUN cp /root/model_server/model_entrypoint.sh /usr/bin/model_entrypoint.sh \
    && chmod +x /usr/bin/model_entrypoint.sh

#ENTRYPOINT ["/bin/bash","/usr/bin/model_entrypoint.sh"]
