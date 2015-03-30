#!/usr/bin/env python
import ROOT
import meta

for name, info in meta.ZHinv_datasets.iteritems() :
    shortname = info['matching_pat'].keys()[0]
    ntuple_total = 0
    with open('datasets/%s.ntuples.txt' % shortname) as filelist :
        for line in filelist :
            f = ROOT.TFile.Open(line.strip())
            hevt = f.Get('ee/eventCount')
            ntuple_total += hevt.GetBinContent(1)

    with open("datasets/"+shortname+".ntuple_eventcount.txt", 'w') as out :
        out.write("%d\n" % ntuple_total)

    das_nevents = info['dbs_info']['nevents']

    print "%9d, %9d : %s" % (ntuple_total, das_nevents, name)
