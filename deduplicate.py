#!/usr/bin/env python
import pickle
import ROOT
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
    left_tree = util.buildChain('datasets/%s.root' % left_dataset, tuple_path)
    right_tree = util.buildChain('datasets/%s.root' % right_dataset, tuple_path)
    left_set = getRunEvtTuples(singlemu)
    print "Built set for %s" % left_dataset
    right_set = getRunEvtTuples(doublemu)
    print "Built set for %s" % right_dataset
    dupes = left_set.intersection(right_set)
    print "Found intersection, pickling. (overlap,sum = %d,%d)" % (len(dupes), len(left_set)+len(right_set))

    with open('datasets/%s.duplicates.pickle' % left_dataset, 'w') as out :
        pickle.dump(dupes, out, 2)

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
        deduplicate(singlemu[i], doublemu[i])
