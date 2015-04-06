#!/usr/bin/env python
import pickle, array, os, sys
import ROOT
ROOT.gROOT.SetBatch(True)
import util

def getRunEvtTuples(chain) :
    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus('run', 1)
    chain.SetBranchStatus('evt', 1)
    tuples = set()
    for i in range(chain.GetEntries()) :
        chain.GetEntry(i)
        tuples.add((chain.run, chain.evt))
    return tuples

def deduplicate(left_dataset, right_dataset, tuple_path) :
    left_tree = util.buildChain('datasets/%s.ntuples.txt' % left_dataset, tuple_path)
    left_set = getRunEvtTuples(left_tree)
    print "Built set for %s" % left_dataset

    right_tree = util.buildChain('datasets/%s.ntuples.txt' % right_dataset, tuple_path)
    right_set = getRunEvtTuples(right_tree)
    print "Built set for %s" % right_dataset

    dupes = left_set.intersection(right_set)
    print "Found intersection, pickling. (overlap,sum = %d,%d)" % (len(dupes), len(left_set)+len(right_set))

    with open('datasets/%s.duplicates.pickle' % left_dataset, 'w') as out :
        pickle.dump(dupes, out, 2)

def makeEntryList(dataset_name, tuple_path) :
    chain = util.buildChain('datasets/%s.ntuples.txt' % dataset_name, tuple_path)
    duplicates = pickle.load(open('datasets/%s.duplicates.pickle' % dataset_name))
    entryList = ROOT.TEntryList('%s_duplicate_entries'%dataset_name, 'Entries in dataset that are in other datasets')

    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus('run', 1)
    chain.SetBranchStatus('evt', 1)
    nentries = chain.GetEntries()
    for i in range(nentries) :
        if i%(nentries/100) == 0 :
            sys.stdout.write('Processing %s: %4.0f%% done.\r' % (dataset_name, i*100./nentries))
            sys.stdout.flush()
        chain.GetEntry(i)
        if (chain.run, chain.evt) in duplicates :
            entryList.Enter(i, chain)

    print 'Made ROOT entry list for ' + dataset_name
    out = ROOT.TFile('datasets/%s.duplicates.root' % dataset_name, 'recreate')
    out.cd()
    entryList.Write()
    out.Close()

if __name__ == '__main__' :
    singlemu = [
        'data_SingleMu_Run2012A_22Jan2013_v1',
        'data_SingleMu_Run2012B_22Jan2013_v1',
        'data_SingleMu_Run2012C_22Jan2013_v1',
        'data_SingleMu_Run2012D_22Jan2013_v1'
    ]

    doublemu = [
        'data_DoubleMu_Run2012A_22Jan2013_v1',
        'data_DoubleMuParked_Run2012B_22Jan2013_v1',
        'data_DoubleMuParked_Run2012C_22Jan2013_v1',
        'data_DoubleMuParked_Run2012D_22Jan2013_v1'
    ]

    for i in range(4) :
        if not os.path.exists('datasets/%s.duplicates.pickle' % singlemu[i]) :
            deduplicate(singlemu[i], doublemu[i], 'mm/final/Ntuple')
        if not os.path.exists('datasets/%s.duplicates.root' % singlemu[i]) :
            makeEntryList(singlemu[i], 'mm/final/Ntuple')
