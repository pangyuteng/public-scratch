FROM tensorflow/tensorflow:2.9.1-gpu-jupyter


RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install git+https://www.github.com/keras-team/keras-contrib.git
RUN pip install tensorflow_addons
