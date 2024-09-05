#!/bin/bash

echo $@

export nnUNet_raw="/radraid/pteng/tmp/nnUNet_raw"
export nnUNet_preprocessed="/radraid/pteng/tmp/nnUNet_preprocessed"
export nnUNet_results="/radraid/pteng/tmp/nnUNet_results"

export TORCH_HOME=/tmp/.torch
export XDG_CACHE_HOME=/tmp/.xdgcache
export TORCH_COMPILE_DEBUG_DIR=/tmp/.torchdebug
export TORCHINDUCTOR_CACHE_DIR=/tmp/.torchinductor
export TRITON_HOME=/tmp/.tritonhome
export TRITON_CACHE_DIR=/tmp/.triton

python -c "import torch;print(torch.__version__)"
nnUNetv2_plan_and_preprocess -d 001 --verify_dataset_integrity

nnUNetv2_train 001 2d 0
