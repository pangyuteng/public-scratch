

```

bash build_and_push.sh

mkdir log

# sample dataset used copied from totalsegmentator.
# for test dataset folder/files, see `sample_dataset.md` and `dataset.json`
# unsure about dataset.json and hola.json, but i just made them to have the same content.

condor_submit condor.sub

condor_tail -f $CLUSTER_ID


```