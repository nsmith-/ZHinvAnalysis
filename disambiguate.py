#!/usr/bin/env python
import ROOT
from meta.ZHinv_datasets import ZHinv_datasets
from array import array
import json
rereco_lumimasks = json.load(open('meta/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt'))

def disambiguate(tree, datatype) :
    ''' Assumes tree is sequential in (run, event)
        If datatype=='data', do lumi mas
    '''
    current_run = 0
    current_evt = 0
    equivalent_entries = {}

    bestCandidate = array('i',[0])
    branch = tree.Branch('bestCandidate', bestCandidate, 'bestCandidate/I')
    lumiMask = array('i',[0])
    lumibranch = tree.Branch('lumiMask', lumiMask, 'lumiMask/I')

    for i in range(tree.GetEntries()) :
        tree.GetEntry(i)
        branch.Fill()
        if datatype == 'data' :
            lumiMask[0] = 0
            runstring = '%d' % tree.run
            if runstring in rereco_lumimasks :
                for mask in rereco_lumimasks[runstring] :
                    if tree.lumi >= mask[0] and tree.lumi <= mask[1] :
                        lumiMask[0] = 1
                        break
            else :
                print runstring
            lumibranch.Fill()
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
    datatype = info['type']
    f = ROOT.TFile("datasets/"+shortname+".root", "update")

    print 'Processing ee path in %s' % shortname
    t = f.Get("ee/Ntuple")
    disambiguate(t, datatype)
    f.cd("ee")
    t.Write("", ROOT.TObject.kOverwrite)

    print 'Processing mm path in %s' % shortname
    t = f.Get("mm/Ntuple")
    disambiguate(t, datatype)
    f.cd("mm")
    t.Write("", ROOT.TObject.kOverwrite)
