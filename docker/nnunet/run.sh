#!/bin/bash

export nnUNet_raw="/radraid/pteng/tmp/test_nnUNet/data/nnUNet_raw"
export nnUNet_preprocessed="/radraid/pteng/test_nnUNet/data/nnUNet_preprocessed"
export nnUNet_results="/radraid/pteng/test_nnUNet/data/nnUNet_results"


python -c "import torch;print(torch.__version__)"