#!/bin/bash

docker build \
  --build-arg GROUPID=$(id -g) \
  --build-arg USERID=$(id -u) \
  --build-arg USERNAME=$USER \
  -t pangyuteng/ml:nnunetv2 .

docker push pangyuteng/ml:nnunetv2
