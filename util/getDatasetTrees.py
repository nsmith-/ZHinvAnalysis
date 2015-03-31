import ROOT
from buildChain import buildChain

def getDatasetTrees(tuplePath, datasets, printInfo=True) :
    trees = {}
    for name, info in datasets.iteritems() :
        shortname = info['matching_pat'].keys()[0]
        tree = None
        # FIXME : hack
        if 'final' not in tuplePath :
            tree = ROOT.TChain(tuplePath)
            filename = "datasets/"+shortname+".root"
            tree.Add(filename)
        else :
            tree = buildChain("datasets/"+shortname+".ntuples.txt", tuplePath)
        with open("datasets/"+shortname+".das_eventcount.txt") as evtcount :
            ntuple_eventcount = int(evtcount.read())
        if datasets[name]['type'] == 'mc' :
            # Adjust weight
            xs = datasets[name]['cross_section']
            if xs < 0 :
                if printInfo : 
                    print "No cross section info for " + name
                xs = 0
            das_nevents = datasets[name]['dbs_info']['nevents']
            dataset_nevents_processed = ntuple_eventcount
            if printInfo :
                print "processed: % 9d, dataset: % 9d, lost: % 3.1f%% : %s" % (dataset_nevents_processed, das_nevents, (das_nevents-dataset_nevents_processed)*100./das_nevents, datasets[name]["name"])
            lumi = 19.6e3 # this was the previous placeholder value
            if 'ee' in tuplePath :
                lumi = 19.238e3
            elif 'mm' in tuplePath :
                lumi = 19.762e3
            weight = lumi*xs/dataset_nevents_processed
            tree.SetWeight(weight, "global")
            if printInfo :
                print "Dataset weight: %f" % weight
        trees[name] = tree
    return trees

