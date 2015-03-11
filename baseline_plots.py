#!/usr/bin/env python
import ROOT
# ROOT.gROOT.SetBatch(ROOT.kTRUE)
from meta.plotgroups import plotgroups, stack_order
from meta.ZHinv_datasets import ZHinv_datasets
import util
import json, os, math

def stackUp(**kwargs) :
  ''' Parameters:
    name
    bins
    xmin
    xmax
    trees
    variable
    cut
    ymin
    ymax
    logY
    xtitle
    ytitle
    (this is more a log of things that need input validation later)
  '''
  name = kwargs['name']
  cut = kwargs['cut'] if 'cut' in kwargs else ''
  if type(cut) is list :
    cut = " && ".join(cut)

  directory = ROOT.TDirectory(name+"_dir", "Helps with TTree::Draw")
  directory.cd()
  canvas = ROOT.TCanvas(name, name)
  mcStack = ROOT.THStack(name+"_hmcstack", "")
  tostack = {}
  todraw = {}

  def findGroupHist(plotgroup) :
    hist_id = "_".join([name, plotgroup, "hist"])
    if directory.Get(hist_id) :
      return directory.Get(hist_id)
    h = ROOT.TH1F(hist_id, plotgroups[plotgroup]['title'], kwargs['bins'], kwargs['xmin'], kwargs['xmax'])
    for optname, optvalue in plotgroups[plotgroup]['histOptions'].iteritems() :
      getattr(h, "Set"+optname)(optvalue)
    return h

  for dataname, info in ZHinv_datasets.iteritems() :
    if dataname not in kwargs['trees'] :
      continue
    plotgroup = info['plotgroup']
    h = findGroupHist(plotgroup)
    hname = h.GetName()
    lumimask = ''
    if info['type'] == 'data' :
        lumimask = ' && lumiMask'
    kwargs['trees'][dataname].Draw(kwargs['variable']+">>+"+hname, cut+lumimask)
    if info['type'] == 'mc' and not 'signal' in info.get('flags',[]) :
      tostack[plotgroup] = h
    elif info['type'] == 'data' :
      todraw[h] = "pex0"
    else :
      todraw[h] = ""

  hstackErrors = ROOT.TH1F("_".join([name, "hstackErrors"]), 'Stat. Error', kwargs['bins'], kwargs['xmin'], kwargs['xmax'])
  hstackErrors.SetDirectory(0)
  hstackErrors.Sumw2()
  hstackErrors.SetFillColor(ROOT.kGray+2)
  hstackErrors.SetFillStyle(3013)
  hstackErrors.SetMarkerSize(0)
  for group in stack_order :
    h = tostack[group]
    h.SetLineColor(ROOT.TColor.GetColorDark(h.GetFillColor()))
    h.SetDirectory(0)
    hstackErrors.Add(h)
    mcStack.Add(h)

  mcStack.Draw()
  mcStack.SetMinimum(kwargs['ymin'])
  mcStack.SetMaximum(kwargs['ymax'])
  mcStack.GetXaxis().SetTitle(kwargs['xtitle'])
  mcStack.GetYaxis().SetTitle(kwargs['ytitle'])

  hstackErrors.Draw("E2 same")

  for h, style in todraw.iteritems() :
    h.SetDirectory(0)
    h.Draw(style+"same")

  if kwargs.get('logY', False) :
    canvas.SetLogy()

  legend = ROOT.TLegend(.55, .75, .92, .88)
  for h in tostack.itervalues() :
    legend.AddEntry(h, h.GetTitle(), "f")
  for h, style in todraw.iteritems() :
    entrystyle = 'l'
    nosame = h.GetDrawOption().replace('same','')
    if 'p' in nosame :
      entrystyle = 'p'
      if 'e' in nosame :
        entrystyle += 'e'
    legend.AddEntry(h, h.GetTitle(), entrystyle)
  legend.SetName(name+"_legend")
  legend.SetNColumns(3)
  legend.SetColumnSeparation(0.1)
  legend.Draw()

  # Transfer object ownership to canvas
  for h in todraw.iterkeys() :
    ROOT.SetOwnership(h, False)
  ROOT.SetOwnership(hstackErrors, False)
  ROOT.SetOwnership(mcStack, False)
  ROOT.SetOwnership(legend, False)
  canvas.GetListOfPrimitives().SetOwner(True)
  return canvas

eetrees = util.getDatasetTrees("ee/Ntuple", ZHinv_datasets)

if not os.path.exists('plots/') :
  os.mkdir('plots')

c = stackUp(name="diLeptonMass",
    bins=50,
    xmin=91-25,
    xmax=91+25,
    trees=eetrees,
    variable="Mass",
    cut='doubleEPass && bestCandidate',
    logY=True,
    ymin=1e-1,
    ymax=1e6,
    xtitle="M_{ll} [GeV]",
    ytitle="Events / 1 GeV")
c.Print("plots/diLeptonMass.pdf")
c.Print("plots/diLeptonMass.root")

cpt = stackUp(name="diLeptonPt",
    bins=50,
    xmin=0,
    xmax=500,
    trees=eetrees,
    variable="Pt",
    cut='doubleEPass && bestCandidate',
    logY=True,
    ymin=1e-2,
    ymax=1e4,
    xtitle="p^{ll}_{T} [GeV]",
    ytitle="Events / 10 GeV")
cpt.Print("plots/diLeptonPt.root")
cpt.Print("plots/diLeptonPt.pdf")

cmet = stackUp(name="reducedMETBalance",
    bins=25,
    xmin=0,
    xmax=5,
    trees=eetrees,
    variable="reducedMET/Pt",
    cut='doubleEPass && bestCandidate',
    logY=True,
    ymin=1e-2,
    ymax=1e4,
    xtitle="#slash{E}_{T}/p^{ll}_{T}",
    ytitle="Events / 0.2")
cmet.Print("plots/METBalance.root")
cmet.Print("plots/METBalance.pdf")
