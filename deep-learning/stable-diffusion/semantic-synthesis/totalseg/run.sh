#!/bin/bash

echo $1 $2

export CODE_FOLDER=$1
export TOTALSEG_FOLDER=$2
cd $CODE_FOLDER
python3 totalseg.py
