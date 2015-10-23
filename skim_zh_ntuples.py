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

mass_string = 'sqrt(pow(m1PtRochCor2012*cosh(m1EtaRochCor2012)+m2PtRochCor2012*cosh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012*sinh(m1EtaRochCor2012)+m2PtRochCor2012*sinh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012,2) - pow(m2PtRochCor2012,2) - 2*m1PtRochCor2012*m2PtRochCor2012*cos(m1PhiRochCor2012-m2PhiRochCor2012))'

cuts = meta.mcuts
cuts += ['doubleMuZHinvPass']
cuts += [
    "abs(%s-91)<10" % mass_string,
    "Pt>50",
    "jetVeto30 < 2",
    "muGlbIsoVetoPt10+eVetoCBIDLoose==0",
    "bjetCSVVetoZHinv==0",
]
baseline = []
print 'Using EntryList for CopyTree'

shortname = sys.argv[1]
inFiles = []
print "Getting input files from %s" % shortname
with open('datasets/%s.ntuples.txt' % shortname) as inList :
    for fn in inList :
        inFiles.append(fn.strip())

outfile = ROOT.TFile('datasets/%s.root' % shortname, "recreate")

entryList_mm = None
if os.path.exists('preselection_plots.root') :
    f = ROOT.TFile.Open('preselection_plots.root')
    entryList_mm = f.Get('%s_%s_baseline' % (shortname, 'mm'))

mergeWithCuts("mm/final/Ntuple", inFiles, baseline, outfile, entryList_mm)
print "Finished copying mm tree for " + shortname

