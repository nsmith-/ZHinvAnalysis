import ROOT
import DataFormats.FWLite as FWLite

from get_das_eventcount import get_pat_file_dict

pat_dict = get_pat_file_dict('DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball')
pat_sum = 0
ntuple_sum = 0
for ntuple_name, pats in pat_dict.iteritems() :
    ntupleFile = ROOT.TFile.Open(ntuple_name)
    if ntupleFile == None :
        continue
    ntupleCount = ntupleFile.Get('ee/eventCount').GetBinContent(1)

    prefix = 'root://cmsxrootd.hep.wisc.edu/'
    patEvents = FWLite.Events(map(lambda fn: prefix+fn, pats))
    patCount = patEvents.size()

    print "PAT: %8d, nTuple: %8d, diff: %5d" % (patCount, ntupleCount, patCount-ntupleCount)
    pat_sum += patCount
    ntuple_sum += ntupleCount

print "Sum pat: %d, sum ntuple: %d" % (pat_sum, ntuple_sum)
