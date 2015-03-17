#!/usr/bin/env python
import pickle, array
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
    left_set = getRunEvtTuples(left_tree)
    print "Built set for %s" % left_dataset

    right_tree = util.buildChain('datasets/%s.root' % right_dataset, tuple_path)
    right_set = getRunEvtTuples(right_tree)
    print "Built set for %s" % right_dataset

    dupes = left_set.intersection(right_set)
    print "Found intersection, pickling. (overlap,sum = %d,%d)" % (len(dupes), len(left_set)+len(right_set))

    with open('datasets/%s.duplicates.pickle' % left_dataset, 'w') as out :
        pickle.dump(dupes, out, 2)

def makeDupeBranch(dataset_name, tuple_path) :
    treefile = ROOT.TFile('datasets/%s.root' % dataset_name, 'update')
    tree = treefile.Get(tuple_path)

    duplicates = pickle.load(open('datasets/%s.duplicates.pickle' % dataset_name))

    duplicate_event = array.array('i',[0])
    branch = tree.Branch('duplicate_event', duplicate_event, 'duplicate_event/I')
    
    for i in range(tree.GetEntries()) :
        tree.GetEntry(i)
        if (tree.run, tree.evt) in duplicates :
            duplicate_event[0] = 1
        else :
            duplicate_event[0] = 0
        branch.Fill()

    treefile.cd(tuple_path[:tuple_path.rfind('/')])
    tree.Write('', ROOT.TObject.kOverwrite)

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
        deduplicate(singlemu[i], doublemu[i], 'mm/Ntuple')
        makeDupeBranch(singlemu[i], 'mm/Ntuple')
