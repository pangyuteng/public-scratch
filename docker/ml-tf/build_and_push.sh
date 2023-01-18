#!/bin/bash

docker build -t pangyuteng/ml:latest .
docker push pangyuteng/ml:latest

#docker tag pangyuteng/ml:latest pangyuteng/ml:tf-2.9.1
#docker push pangyuteng/ml:tf-2.9.1