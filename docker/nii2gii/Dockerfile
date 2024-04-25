FROM pangyuteng/dcm:latest


RUN apt-get update && apt-get install build-essential make vim -yq
WORKDIR /opt
RUN git clone https://github.com/neurolabusc/nii2mesh
RUN cd nii2mesh/src && make
