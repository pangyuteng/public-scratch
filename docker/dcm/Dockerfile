FROM tensorflow/tensorflow:2.9.1-gpu-jupyter

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 build-essential make vim curl wget -yq

WORKDIR /opt
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb && \
    apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb -yq

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install vtk-osmesa --extra-index-url https://gitlab.kitware.com/api/v4/projects/13/packages/pypi/simple

WORKDIR /opt
RUN git clone https://github.com/neurolabusc/nii2mesh
RUN cd nii2mesh/src && make && mv /opt/nii2mesh/src/nii2mesh /usr/bin

