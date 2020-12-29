FROM centos
FROM java:8


SHELL["/bin/bash","-c"]

USER root

LABEL "date"="2020-12"
LABEL "register"="root" \
"password"="l8X6%WAqc9ifGX6o" \
"link"="140.210.92.100"

#--build-arg <varname>=<value>
ARG builder=wmingzhu

ONBUILD RUN ls -al

HEALTHCHECK --interval=30m --timeout=5s CMD curl -f http://localhost/ || exit 1

COPY model-server /root/model-server/

WORKDIR /root/model-server

ENV MODEL_BASE_PATH=/models

RUN mkdir -p ${MODEL_BASE_PATH}

#应该在docker run的时候明确指定宿主机目录，这里
VOLUME model-server

# gRPC
EXPOSE 8500
# REST
EXPOSE 8501

RUN ls -l /root/model-server/model_entrypoint.sh
RUN cp /root/model-server/model_entrypoint.sh /usr/bin/model_entrypoint.sh \
    && chmod +x /usr/bin/model_entrypoint.sh

ENTRYPOINT ["/usr/bin/model_entrypoint.sh"]
