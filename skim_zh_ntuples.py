#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import sys, os

def mergeWithCuts(treeName, fileNames, selections, outFile) :
  '''
  Merges trees named treeName from files using && of selection array
  Returns TDirectory
  '''
  # expects fsa style directory
  outDir = outFile.mkdir(treeName.split('/')[0])
  chain = ROOT.TChain(treeName)
  for fileName in fileNames :
    chain.Add(fileName)
  outDir.cd()
  print "Starting tree copy..."
  outTree = chain.CopyTree("&&".join(selections))
  print "Done"
  outTree.Write()
  cutInfo = ROOT.TH1F("cutSummary", "Cut Summary", 2, 0, 1)
  cutInfo.SetBinContent(1, chain.GetEntries())
  cutInfo.SetBinContent(2, outTree.GetEntries())
  labels = ["All events", "Passed events"]
  for i in range(len(labels)) :
    cutInfo.GetXaxis().SetBinLabel(i+1, labels[i])
  cutInfo.Write()

eID = [
  "Pt > 20",
  "CBID_MEDIUM==1",
]
muID = [
  "Pt > 20",
  "IsGlobal==1",
  "IsTracker==1",
  "MuonHits>0",
  "MatchedStations>1",
  "TkLayersWithMeasurement>5",
  "PixHits>0",
  "NormTrkChi2<10",
  "PVDXY<.2",
  "PVDZ<.5",
  "RelPFIsoDBDefault<.2"
]

ecuts = [leg+cut for leg in ("e1","e2") for cut in eID]
mcuts = [leg+cut for leg in ("m1","m2") for cut in muID]
baseline = [
  "abs(Mass-91)<25",
  "Pt>30",
  "reducedMET>50"
]

inFiles = []
print "Getting input files from %s" % os.getenv('INPUT')
with open(os.getenv('INPUT')) as inList :
  for fn in inList :
    inFiles.append(fn.strip())

outfile = ROOT.TFile(os.getenv('OUTPUT'), "recreate")
mergeWithCuts("ee/final/Ntuple", inFiles, ecuts+baseline, outfile)
mergeWithCuts("mm/final/Ntuple", inFiles, mcuts+baseline, outfile)

