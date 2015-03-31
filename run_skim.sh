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
  if [ ! -f datasets/${dataset}.root ]; then
    INPUT="datasets/${dataset}.ntuples.txt" OUTPUT="datasets/${dataset}.root" ./skim_zh_ntuples.py 2>/dev/null
  fi
  if [ ! -f datasets/${dataset}.das_eventcount.txt ]; then
    ./read_das_eventcount.py ${dataset} > datasets/${dataset}.das_eventcount.txt
  fi
done

# Lumi for data datasets
pushd meta
if [ ! -f DoubleElectron.lumi.txt ]; then
  /afs/hep.wisc.edu/cms/cmsprod/farmoutCmsJobs/jobReportSummary.py --json-out DoubleElectron.json `find /nfs_scratch/nsmith/ZHinvNtuples/data_DoubleElectron* -name *.xml`
  lumiCalc2.py -i DoubleElectron.json overview > DoubleElectron.lumi.txt
fi
if [ ! -f Muon.lumi.txt ]; then
  /afs/hep.wisc.edu/cms/cmsprod/farmoutCmsJobs/jobReportSummary.py --json-out Muon.json `find /nfs_scratch/nsmith/ZHinvNtuples/data_*Mu* -name *.xml`
  lumiCalc2.py -i Muon.json overview > Muon.lumi.txt
fi
popd
