#!/bin/env python
import json, os, subprocess

# MC DAS paths, referenced by primary dataset name
ZHinv_datasets = {
    # W + Jets MC samples
    "W1JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM",
        "cross_section" : 6441.4,
        "plotgroup" : "WToLNu"
    }, 
    "W2JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM",
        "cross_section" : 2087.5,
        "plotgroup" : "WToLNu"
    }, 
    "W3JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM",
        "cross_section" : 619.1,
        "plotgroup" : "WToLNu"
    }, 
    "W4JetsToLNu_TuneZ2Star_8TeV-madgraph": {
        "name": "/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 255.3,
        "plotgroup" : "WToLNu"
    }, 

    # WGamma
    "WGToLNuG_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/WGToLNuG_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 461.6,
        "plotgroup" : "WToLNu"
    }, 

    # Z -> LL samples (large!)
    "DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball": {
        "name": "/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 3532.8,
        "plotgroup" : "ZToLL"
    },
    "DYJetsToLL_M-10To50filter_8TeV-madgraph": {
        "name": "/DYJetsToLL_M-10To50filter_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 860.5,
        "plotgroup" : "ZToLL"
    }, 
    "ZG_Inclusive_8TeV-madgraph": {
        "name": "/ZG_Inclusive_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 123.9,
        "plotgroup" : "ZToLL"
    }, 

    # double top
    "TTJets_FullLeptMGDecays_8TeV-madgraph-tauola": {
        "name": "/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM",
        "cross_section" : 23.89,
        "plotgroup" : "ttbar"
    }, 
    "TTWJets_8TeV-madgraph": {
        "name": "/TTWJets_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 0.232,
        "plotgroup" : "ttbar"
    }, 
    "TTZJets_8TeV-madgraph_v2": {
        "name": "/TTZJets_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 0.208,
        "plotgroup" : "ttbar"
    }, 

    # single top 
    "T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": {
        "name": "/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 11.1,
        "plotgroup" : "singleTop"
    }, 

    # single anti-top
    "Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola": {
        "name": "/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 11.1,
        "plotgroup" : "singleTop"
    }, 

    # VV backgrounds
    "WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/WWJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 5.995,
        "plotgroup" : "WW"
    }, 
    "WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola": {
        "name": "/WZJetsTo3LNu_TuneZ2_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "cross_section" : 1.057,
        "plotgroup" : "WZ"
    }, 

    # Irred. background
    "ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola": {
        "name": "/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM",
        "cross_section" : .380,
        "plotgroup" : "ZZ"
    }, 

    # Signal
    "ZH_ZToLL_HToInv_M-125_8TeV-pythia6": {
        "name": "/ZH_ZToLL_HToInv_M-125_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "plotgroup" : "signal",
        "cross_section" : 0.0398,
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
    info['plotgroup'] = "data"
  ZHinv_datasets.update(dataset)

def getDBSInfo(das_path) :
  query = 'summary dataset=%s' % das_path
  cmd = ['das_client.py',
      '--format=json',
      '--query="%s"' % query]
  output = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE).stdout
  result = json.load(output)
  if result['status'] == 'ok' and result['nresults'] == 1 :
    return result['data'][0]['summary'][0]
  else :
    return None

# Load any extra information that we may have collected
json_location = os.path.dirname(os.path.realpath(__file__))+"/ZHinv_datasets.json"
if os.path.exists(json_location) :
  with open(json_location) as f :
    extras = json.load(f)
    for key in ZHinv_datasets.iterkeys() :
      if key in extras :
        if 'matching_pat' in extras[key] :
          ZHinv_datasets[key]['matching_pat'] = extras[key]['matching_pat']
        # 'matching_pat' filled from match_PAT.py

        if 'dbs_info' in extras[key] :
          ZHinv_datasets[key]['dbs_info'] = extras[key]['dbs_info']
        else :
          ZHinv_datasets[key]['dbs_info'] = getDBSInfo(ZHinv_datasets[key]['name'])

if __name__ == "__main__" :
  print json.dumps(ZHinv_datasets, indent=4)
