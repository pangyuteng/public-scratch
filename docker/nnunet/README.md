
### how to run condor jobs with PYTorch container in HTCondor as non-root.

Q: how do you run torch (or nnUnet) code in a docker container in htcondor as non-root?

A: set below set of environment variables:


```
export TORCH_HOME=/tmp/.torch
export XDG_CACHE_HOME=/tmp/.xdgcache
export TORCH_COMPILE_DEBUG_DIR=/tmp/.torchdebug
export TORCHINDUCTOR_CACHE_DIR=/tmp/.torchinductor
export TRITON_HOME=/tmp/.tritonhome
export TRITON_CACHE_DIR=/tmp/.triton

```


+ notes and files used to test above solution is commited in this folder.

```


bash build_and_push.sh

mkdir log

# sample dataset used copied from totalsegmentator.
# for test dataset folder/files, see `sample_dataset.md` and `dataset.json`
# unsure about dataset.json and hola.json, but i just made them to have the same content.
nnUNet_raw/Dataset001_hola/dataset.json
nnUNet_preprocessed/Dataset001_hola/dataset.json

condor_submit condor.sub

condor_tail -f $CLUSTER_ID


```

+ read more here: https://chtc.cs.wisc.edu/uw-research-computing/machine-learning-htc
