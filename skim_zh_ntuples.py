#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
import meta
import sys, os

def mergeWithCuts(treeName, fileNames, selections, outFile, entryList=None) :
    # expects fsa style directory
    outDir = outFile.mkdir(treeName.split('/')[0])
    chain = ROOT.TChain(treeName)
    for fileName in fileNames :
        chain.Add(fileName)
    if entryList :
        chain.SetEntryList(entryList)
    outDir.cd()
    outTree = chain.CopyTree("&&".join(selections))
    outTree.Write()
    cutInfo = ROOT.TH1F("cutSummary", "Cut Summary", 2, 0, 1)
    cutInfo.SetBinContent(1, chain.GetEntries())
    cutInfo.SetBinContent(2, outTree.GetEntries())
    labels = ["All events", "Passed events"]
    for i in range(len(labels)) :
        cutInfo.GetXaxis().SetBinLabel(i+1, labels[i])
    cutInfo.Write()

baseline = [
    "abs(Mass-91)<25",
    "Pt>30",
    "reducedMET>50"
]

shortname = sys.argv[1]
inFiles = []
print "Getting input files from %s" % shortname
with open('datasets/%s.ntuples.txt' % shortname) as inList :
    for fn in inList :
        inFiles.append(fn.strip())

outfile = ROOT.TFile('datasets/%s.root' % shortname, "recreate")

entryList_ee = None
entryList_mm = None
if os.path.exists('preselection_plots.root') :
    f = ROOT.TFile.Open('preselection_plots.root')
    entryList_ee = f.Get('%s_%s_preselection' % (shortname, 'ee'))
    entryList_mm = f.Get('%s_%s_preselection' % (shortname, 'mm'))

mergeWithCuts("ee/final/Ntuple", inFiles, baseline, outfile, entryList_ee)
print "Finished copying ee tree for " + shortname
mergeWithCuts("mm/final/Ntuple", inFiles, baseline, outfile, entryList_mm)
print "Finished copying mm tree for " + shortname

