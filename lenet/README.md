```
# -u $(id -u):$(id -g) 

docker run -it -p 8888:8888 -v /cvibraid:/cvibraid -w $PWD --runtime=nvidia tensorflow/tensorflow:2.10.0-gpu-jupyter bash

pip install tensorflow_datasets

CUDA_VISIBLE_DEVICES=3 python train.py

```

```

https://web.archive.org/web/20100730053801id_/http://srl.csdl.tamu.edu/courses/SR2008/papers/others/LeCun.pdf
https://www.tensorflow.org/datasets/keras_example
https://en.wikipedia.org/wiki/LeNet

```