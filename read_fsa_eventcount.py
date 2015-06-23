#!/usr/bin/env python
import ROOT
import meta
import os

print "FSA total, DAS total, Dataset total : Name"
print "------------------------------------------"

for name, info in meta.ZHinv_datasets.iteritems() :
    shortname = info['matching_pat'].keys()[0]
    if os.path.exists("datasets/"+shortname+".ntuple_eventcount.txt") :
        continue
    ntuple_total = 0
    with open('datasets/%s.ntuples.txt' % shortname) as filelist :
        for line in filelist :
            f = ROOT.TFile.Open(line.strip())
            hevt = f.Get('ee/skimCounter')
            ntuple_total += hevt.Integral()

    with open("datasets/"+shortname+".ntuple_eventcount.txt", 'w') as out :
        out.write("%d\n" % ntuple_total)

    total_nevents = info['dbs_info']['nevents']

    das_eventcount = 0
    if os.path.exists("datasets/"+shortname+".das_eventcount.txt") :
        with open("datasets/"+shortname+".das_eventcount.txt") as evtcount :
            das_eventcount = int(evtcount.read())

    if info['type'] == 'data' :
        print "**%9d, %9d, %9d : %s" % (ntuple_total, das_eventcount, total_nevents, name)
    else :
        print "%9d, %9d, %9d : %s" % (ntuple_total, das_eventcount, total_nevents, name)

print "** = FSA applies run certification JSON"
