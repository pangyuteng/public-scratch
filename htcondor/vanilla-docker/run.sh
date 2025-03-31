#!/bin/bash

docker run -u $(id -u):$(id -u) -p 80:80 kennethreitz/httpbin