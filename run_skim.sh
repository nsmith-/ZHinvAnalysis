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
    ./skim_zh_ntuples.py ${dataset} 2>/dev/null &
  fi
  if [ ! -f datasets/${dataset}.das_eventcount.txt ]; then
    ./read_das_eventcount.py ${dataset} > datasets/${dataset}.das_eventcount.txt
  fi
  while [[ `jobs|wc -l` -gt 7 ]]; do sleep 30; done;
done
wait

# Lumi for data datasets
pushd meta
if [ ! -f DoubleElectron.lumi.txt ]; then
  /afs/hep.wisc.edu/cms/cmsprod/farmoutCmsJobs/jobReportSummary.py --json-out DoubleElectron.json `find /nfs_scratch/nsmith/ZHinvNtuples/data_DoubleElectron* -name *.xml`
  lumiCalc2.py -i DoubleElectron.json overview > DoubleElectron.lumi.txt
fi
if [ ! -f DoubleElectron.pileup.root ]; then
  pileupCalc.py \
    -i DoubleElectron.json \
    --inputLumiJSON pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr_v2.txt \
    --calcMode true \
    --minBiasXsec 69400 \
    --maxPileupBin 60 \
    --numPileupBins 60 \
    DoubleElectron.pileup.root 
fi
if [ ! -f Muon.lumi.txt ]; then
  /afs/hep.wisc.edu/cms/cmsprod/farmoutCmsJobs/jobReportSummary.py --json-out Muon.json `find /nfs_scratch/nsmith/ZHinvNtuples/data_*Mu* -name *.xml`
  lumiCalc2.py -i Muon.json overview > Muon.lumi.txt
fi
if [ ! -f Muon.pileup.root ]; then
  pileupCalc.py \
    -i Muon.json \
    --inputLumiJSON pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr_v2.txt \
    --calcMode true \
    --minBiasXsec 69400 \
    --maxPileupBin 60 \
    --numPileupBins 60 \
    Muon.pileup.root 
fi
popd

if [ ! -f mcPileup.root ]; then
  ./mcPileupCalc.py > meta/pileupReweight.py
fi
