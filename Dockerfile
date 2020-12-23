FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]



RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse' > /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse' >> /etc/apt/sources.list


RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libsm6 \
        libxrender1 \
        libxext6 \
        libglib2.0-0 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*



RUN pip3 --no-cache-dir install --upgrade pip setuptools \
    -i https://pypi.douban.com/simple \
    && pip config set global.index-url https://pypi.douban.com/simple \
    && pip --no-cache-dir install torch==1.5.0+cpu torchvision==0.6.0+cpu \
   -f https://download.pytorch.org/whl/torch_stable.html \
   && pip --no-cache-dir install tensorflow==2.0 onnxruntime pypmml flask requests pillow \
   opencv-python gunicorn



RUN ln -s /usr/bin/python3 /usr/bin/python


ADD jdk-8u181-linux-x64.tar.gz /usr/local
COPY model-server /root/model-server

WORKDIR /root/model-server


# Set where models should be stored in the container
ENV MODEL_BASE_PATH=/models
RUN mkdir -p ${MODEL_BASE_PATH}


# The only required piece is the model name in order to differentiate endpoints

ENV LANG=C.UTF-8
ENV JAVA_HOME /usr/local/jdk1.8.0_181
ENV PATH $JAVA_HOME/bin:$PATH


# gRPC
EXPOSE 8500
# REST
EXPOSE 8501


#RUN echo -e "#!/bin/bash \n \
#python3 /root/model-server/run.py" > /usr/bin/model_entrypoint.sh \
#&& chmod +x /usr/bin/model_entrypoint.sh

RUN cp /root/model-server/model_entrypoint.sh /usr/bin/model_entrypoint.sh \
    && chmod +x /usr/bin/model_entrypoint.sh

# Create a script that runs the model server so we can use environment variables
# while also passing in arguments from the docker command line

ENTRYPOINT ["/usr/bin/model_entrypoint.sh"]
