#!/bin/bash
docker build -t pangyuteng/ml:torch .

docker push pangyuteng/ml:torch
