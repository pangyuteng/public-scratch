#!/bin/bash

export nnUNet_raw="/radraid/pteng/tmp/nnUNet_raw"
export nnUNet_preprocessed="/radraid/pteng/tmp/nnUNet_preprocessed"
export nnUNet_results="/radraid/pteng/tmp/nnUNet_results"

python -c "import torch;print(torch.__version__)"
nnUNetv2_plan_and_preprocess -d 001 --verify_dataset_integrity
nnUNetv2_train 001 2d 0
