ARG TF_TAG=1.15.0-gpu-py3
FROM tensorflow/tensorflow:$TF_TAG
RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN pip install --prefer-binary opencv-python-headless albumentations
# RUN pip install 
