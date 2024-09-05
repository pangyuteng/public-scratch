FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-devel

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt update && apt install git -yq
RUN pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git

ENV TORCH_HOME=/tmp/.torch
ENV XDG_CACHE_HOME=/tmp/.xdgcache

ARG GROUPID
ARG USERID
ARG USERNAME

USER root
RUN groupadd -g ${GROUPID} mygroup
RUN useradd --no-log-init -u ${USERID} -g ${GROUPID} -s /bin/bash -md /home/${USERNAME} ${USERNAME}
RUN usermod -a -G ${GROUPID} ${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}
