#!/usr/bin/env python
import ROOT
from meta.ZHinv_datasets import ZHinv_datasets
from array import array

def disambiguate(tree) :
    ''' Assumes tree is sequential in (run, event)
    '''
    current_run = 0
    current_evt = 0
    equivalent_entries = {}

    bestCandidate = array('i',[0])
    branch = tree.Branch('bestCandidate', bestCandidate, 'bestCandidate/I')

    for i in range(tree.GetEntries()) :
        tree.GetEntry(i)
        branch.Fill()
        if current_run == 0 :
            current_run = tree.run
            current_evt = tree.evt
        if tree.run != current_run or tree.evt != current_evt :
            best = equivalent_entries.keys()[0]
            for index, values in equivalent_entries.iteritems() :
                if values['ZCompatibility'] < equivalent_entries[best]['ZCompatibility'] :
                    best = index
            cachedEntry = tree.GetReadEntry()
            tree.GetEntry(best)
            bestCandidate[0] = 1
            branch.Fill()
            bestCandidate[0] = 0
            tree.GetEntry(cachedEntry)
            equivalent_entries = {}
            current_run = tree.run
            current_evt = tree.evt
        equivalent_entries[i] = {'ZCompatibility' : abs(tree.Mass-91)}

for name, info in ZHinv_datasets.iteritems() :
    shortname = info['matching_pat'].keys()[0]
    f = ROOT.TFile("datasets/"+shortname+".root", "update")

    print 'Processing ee path in %s' % shortname
    t = f.Get("ee/Ntuple")
    disambiguate(t)
    f.cd("ee")
    t.Write("", ROOT.TObject.kOverwrite)

    print 'Processing mm path in %s' % shortname
    t = f.Get("mm/Ntuple")
    disambiguate(t)
    f.cd("mm")
    t.Write("", ROOT.TObject.kOverwrite)
