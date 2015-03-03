#!/bin/env python

# MC DAS paths, referenced by primary dataset name
ZHinv_datasets = {
    # W + Jets MC samples
    "W1JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"
    }, 
    "W2JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"
    }, 
    "W3JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"
    }, 
    "W4JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # WGamma
    "WGToLNuG_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/WGToLNuG_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # Z -> LL samples (large!)
    "DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball": {
        "name": "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    },
    "DYJetsToLL_M-10To50filter_8TeV-madgraph": {
        "name": "/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 
    "ZG_Inclusive_8TeV-madgraph": {
        "name": "/ZG_Inclusive_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # double top
    "TTJets_FullLeptMGDecays_8TeV-madgraph-tauola": {
        "name": "/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM"
    }, 
    "TTWJets_8TeV-madgraph": {
        "name": "/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 
    "TTZJets_8TeV-madgraph_v2": {
        "name": "/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # single top 
    "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": {
        "name": "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # single anti-top
    "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": {
        "name": "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # VV backgrounds
    "WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 
    "WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola": {
        "name": "/WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"
    }, 

    # Irred. background
    "ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM"
    }, 

    # Signal
    "ZH_ZToLL_HToInv_M-125_8TeV-pythia6": {
        "name": "/ZH_ZToLL_HToInv_M-125_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "flags": ['signal']
    } 
}
# Mark mc type
for info in ZHinv_datasets.itervalues() :
  info['type'] = "mc"

# Data Samples ------------------------
primaryDatasets = ['DoubleElectron', 'DoubleMu', 'SingleMu']
for PD in primaryDatasets :
  parked = ""
  if PD == "DoubleMu" :
    parked = "Parked"
  dataset = {
    "%s_Run2012A" % PD : {
        "name" : "/%s/Run2012A-22Jan2013-v1/AOD" % PD
    },
    "%s_Run2012B" % (PD+parked) : {
        "name" : "/%s/Run2012B-22Jan2013-v1/AOD" % (PD+parked)
    },
    "%s_Run2012C" % (PD+parked) : {
        "name" : "/%s/Run2012C-22Jan2013-v1/AOD" % (PD+parked)
    },
    "%s_Run2012D" % (PD+parked) : {
        "name" : "/%s/Run2012D-22Jan2013-v1/AOD" % (PD+parked)
    }
  }
  for info in dataset.itervalues() :
    info['type'] = "data"
  ZHinv_datasets.update(dataset)

if __name__ == "__main__" :
  print "Z(ll) H(inv.) dataset summary --------"
  for name, info in ZHinv_datasets.iteritems() :
    print "%s (type %s, flags: %s)" % (name, info['type'], ",".join(info.get('flags','')))
