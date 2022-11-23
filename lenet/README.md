```

throwback wednesday exercise from jhoffman

# -u $(id -u):$(id -g) 

docker run -it -p 8888:8888 -w $PWD -v $PWD:$PWD --runtime=nvidia tensorflow/tensorflow:2.10.0-gpu-jupyter bash

pip install tensorflow_datasets

# attempting to replicate the original lenet - loss not dropping
CUDA_VISIBLE_DEVICES=3 python lenet-sgd-sigmoid.py

# loss dropping within 10 epochs
CUDA_VISIBLE_DEVICES=3 python lenet-sgd-tanh.py
CUDA_VISIBLE_DEVICES=3 python lenet-adam-sigmoid.py

```

```

https://web.archive.org/web/20100730053801id_/http://srl.csdl.tamu.edu/courses/SR2008/papers/others/LeCun.pdf
https://www.tensorflow.org/datasets/keras_example
https://en.wikipedia.org/wiki/LeNet

```