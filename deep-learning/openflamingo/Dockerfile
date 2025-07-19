
# worked # FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
# didnt work #FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
#FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel
#RUN apt-get update && apt-get install vim curl -yq

# Copy the package requirements
COPY requirements.txt /opt

WORKDIR /opt
# Install the package requirements
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN mkdir /.local && chmod 777 -R /.local
