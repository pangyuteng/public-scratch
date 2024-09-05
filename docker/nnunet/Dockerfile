FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-devel

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt update && apt install git -yq
RUN pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git

RUN pip install SimpleITK==2.2.1