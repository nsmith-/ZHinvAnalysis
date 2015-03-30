import ROOT
import DataFormats.FWLite as FWLite

prefix = 'root://cmsxrootd.hep.wisc.edu/'

ntuple = '/store/user/nsmith/ZHinvNtuples/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/make_ntuples_cfg-patTuple_cfg-00037C53-AAD1-E111-B1BE-003048D45F38.root'
ntupleFile = ROOT.TFile.Open(prefix+ntuple)
ntupleCount = ntupleFile.Get('ee/eventCount').GetBinContent(1)

pattuples = [
    '/store/user/dntaylor/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/Fall2014PATTuples_V1/patTuple_cfg-00037C53-AAD1-E111-B1BE-003048D45F38.root',
    '/store/user/dntaylor/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/Fall2014PATTuples_V1/patTuple_cfg-00050BBE-D5D2-E111-BB65-001E67398534.root',
    '/store/user/dntaylor/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/Fall2014PATTuples_V1/patTuple_cfg-0035C962-7DD4-E111-B659-001E6739672F.root',
    '/store/user/dntaylor/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/Fall2014PATTuples_V1/patTuple_cfg-00579DEC-2BD3-E111-8D68-001E673973D2.root'
]
patEvents = FWLite.Events(map(lambda s: prefix+s, pattuples))
patCount = patEvents.size()

print "PAT: %d, nTuple: %d" % (patCount, ntupleCount)
