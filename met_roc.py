#!/bin/env python
import ROOT

def buildChain(fileListName, ntupleName) :
  chain = ROOT.TChain(ntupleName)
  with open(fileListName) as fileList :
    nfiles = 0
    for fileName in fileList :
      chain.Add(fileName.strip())
      nfiles += 1
      if nfiles > 40 :
        break
  return chain

signalChain = buildChain('datasets/ZZJetsTo2L2Nu_TuneZ2star_8TeV-madgraph-tauola.ntuples.txt', 'ee/final/Ntuple')
backgroundChain = buildChain('datasets/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball.ntuples.txt', 'ee/final/Ntuple')

def buildROC(var) :
  plotdir = ROOT.TDirectory("roc","roc")
  plotdir.cd()

  signalChain.Draw("%s >> signal_hist(100,0,50)" % var)
  signal_hist = plotdir.Get("signal_hist")
  backgroundChain.Draw("%s >> background_hist(100,0,50)" % var)
  background_hist = plotdir.Get("background_hist")

  roc = ROOT.TGraph(101)
  x = []
  y = []
  sig_int = 0
  bkg_int = 0
  for i in reversed(range(1,102)) :
    sig_int += signal_hist.GetBinContent(i)
    bkg_int += background_hist.GetBinContent(i)
    x.append(sig_int)
    y.append(bkg_int)

  for i in range(0,101) :
    roc.SetPoint(i, x[i]/sig_int, y[i]/bkg_int)

  roc.SetName("roc_%s" % var)
  return roc

redmet = buildROC("reducedMET")
redmet.SetLineColor(ROOT.kRed)
redmet.SetMarkerColor(ROOT.kRed)
redmet.SetTitle("Reduced MET")
pfmet = buildROC("type1_pfMetEt")
pfmet.SetTitle("Type 1 PF MET")

g = ROOT.TMultiGraph()
g.Add(redmet, "lp")
g.Add(pfmet, "lp")
g.Draw("a")
g.GetXaxis().SetTitle("ZZ#rightarrow2l2#nu Efficiency")
g.GetYaxis().SetTitle("Z+Jets Efficiency")
