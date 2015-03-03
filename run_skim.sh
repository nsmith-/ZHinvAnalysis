#!/bin/bash

mkdir -p datasets
for dataset in `cat ~/public_html/ZHInv/to_ntuplize.txt`; do
  if [ ! -f datasets/${dataset}.root ]; then
    find /hdfs/store/user/nsmith/ZHinvNtuples/${dataset}/ -name \*.root | sed 's:/hdfs:root\://cmsxrootd.hep.wisc.edu/:' > datasets/${dataset}.files.txt
    INPUT="datasets/${dataset}.files.txt" OUTPUT="datasets/${dataset}.root" ./skim_zh_ntuples.py 2>/dev/null
  fi
done


