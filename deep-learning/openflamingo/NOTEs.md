

git clone git@hf.co:spaces/openflamingo/OpenFlamingo

docker build -t pangyuteng/hf-test .
docker run -it -p 7860:7860 -v $PWD:/opt pangyuteng/hf-test bash

docker run --env-file=.env -it --gpus device=0 -p 7860:7860 \
-u $(id -u):$(id -g) -w $PWD -v /radraid:/radraid pangyuteng/hf-test bash



https://huggingface.co/openflamingo/OpenFlamingo-4B-vitl-rpj3b/blob/main/README.md
