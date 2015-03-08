#!/bin/bash

# This makes a bunch of files in datasets with some associated
# production information

mkdir -p datasets
for dataset in `cat meta/sample_shortnames.txt`; do
  if [ ! -f datasets/${dataset}.ntuples.txt ]; then
    find /hdfs/store/user/nsmith/ZHinvNtuples/${dataset}/ -name \*.root | sed 's:/hdfs:root\://cmsxrootd.hep.wisc.edu/:' > datasets/${dataset}.ntuples.txt
  fi
  if [ ! -f datasets/${dataset}.pattuples.txt ]; then
    find /nfs_scratch/nsmith/ZHinvNtuples/${dataset}/submit -type f -name submit -exec sed -n 's/^Arguments *= "\(.*\)"$/\1/p' '{}' \; > datasets/${dataset}.pattuples.txt
  fi
  if [ ! -f datasets/${dataset}.missing_events.txt ]; then
    ./get_missing_event_count.py ${dataset} > datasets/${dataset}.missing_events.txt
  fi
  if [ ! -f datasets/${dataset}.root ]; then
    INPUT="datasets/${dataset}.ntuples.txt" OUTPUT="datasets/${dataset}.root" ./skim_zh_ntuples.py 2>/dev/null
  fi
done


