import ROOT
import util

def getRunEvtTuples(chain) :
    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus('run', 1)
    chain.SetBranchStatus('evt', 1)
    tuples = []
    for i in range(chain.GetEntries()) :
        chain.GetEntry(i)
        tuples.append((chain.run, chain.evt))
    return tuples

singlemu = util.buildChain('datasets/data_SingleMu_Run2012A_22Jan2013_v1.ntuples.txt', 'mm/final/Ntuple')
doublemu = util.buildChain('datasets/data_DoubleMu_Run2012A_22Jan2013_v1.ntuples.txt', 'mm/final/Ntuple')
single = getRunEvtTuples(singlemu)
double = getRunEvtTuples(doublemu)
dupes = set(single).intersection(double)
print dupes
