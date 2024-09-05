#!/bin/bash

echo $@

export nnUNet_raw="/radraid/pteng/tmp/nnUNet_raw"
export nnUNet_preprocessed="/radraid/pteng/tmp/nnUNet_preprocessed"
export nnUNet_results="/radraid/pteng/tmp/nnUNet_results"

#export TORCH_LOGS="+dynamo"
#export TORCHDYNAMO_VERBOSE=1
#export TRITON_HOME=/tmp
export TRITON_CACHE_DIR=/tmp
# python -c "import torch;print(torch.__version__)"
# nnUNetv2_plan_and_preprocess -d 001 --verify_dataset_integrity

nnUNetv2_train 001 2d 0
