import ROOT

def getDatasetTrees(tuplePath, datasets, printInfo=True) :
    trees = {}
    for name, info in datasets.iteritems() :
        shortname = info['matching_pat'].keys()[0]
        tree = ROOT.TChain(tuplePath)
        filename = "datasets/"+shortname+".root"
        tree.Add(filename)
        with open("datasets/"+shortname+".missing_events.txt") as misscount :
            missing_events = int(misscount.read())
        if datasets[name]['type'] == 'mc' :
            # Adjust weight
            xs = datasets[name]['cross_section']
            if xs < 0 :
                if printInfo : 
                    print "No cross section info for " + name
                xs = 0
            nevents = tree.GetEntries()
            das_nevents = datasets[name]['dbs_info']['nevents']
            dataset_nevents_processed = das_nevents - missing_events
            if printInfo :
                print "pass: % 8d, processed: % 9d, dataset: % 9d, lost: % 3.1f%% : %s" % (nevents, dataset_nevents_processed, das_nevents, missing_events*100./das_nevents, datasets[name]["name"])
            if nevents > 0 :
                weight = 19.6e3*xs/dataset_nevents_processed
                tree.SetWeight(weight, "global")
                if printInfo :
                    print "Dataset weight: %f" % weight
        trees[name] = tree
    return trees

