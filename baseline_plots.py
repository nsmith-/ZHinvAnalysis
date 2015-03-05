#!/bin/env python
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from meta.plotgroups import plotgroups, stack_order
from meta.ZHinv_datasets import ZHinv_datasets
import json, os

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
    kwargs['trees'][dataname].Draw(kwargs['variable']+">>+"+hname, kwargs['cut'] if 'cut' in kwargs else '')
    if info['type'] == 'mc' and not 'signal' in info.get('flags',[]) :
      tostack[plotgroup] = h
    elif info['type'] == 'data' :
      todraw[h] = "pex0"
    else :
      todraw[h] = ""

  for group in stack_order:
    h = tostack[group]
    # Hack until I get a better legend builder
    h.SetLineColor(h.GetFillColor())
    h.SetMarkerColor(h.GetFillColor())
    h.SetDirectory(0)
    mcStack.Add(h)
  mcStack.Draw()
  mcStack.SetMinimum(kwargs['ymin'])
  mcStack.SetMaximum(kwargs['ymax'])
  mcStack.GetXaxis().SetTitle(kwargs['xtitle'])
  mcStack.GetYaxis().SetTitle(kwargs['ytitle'])

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
  ROOT.SetOwnership(mcStack, False)
  ROOT.SetOwnership(legend, False)
  canvas.GetListOfPrimitives().SetOwner(True)
  return canvas

files = {}
for name, info in ZHinv_datasets.iteritems() :
  # No data for now
  # if ZHinv_datasets[name]['type'] == 'data' :
  #   continue
  tuplename = info['matching_pat'].keys()[0]
  f = ROOT.TFile("datasets/"+tuplename+".root")
  files[name] = f

eetrees = {}
for name, tfile in files.iteritems() :
  tree = tfile.Get("ee/Ntuple")
  if ZHinv_datasets[name]['type'] == 'mc' :
    # Adjust weight
    xs = ZHinv_datasets[name]['cross_section']
    if xs < 0 :
      print "No cross section info for " + name
      xs = 0
    nevents = tfile.Get("ee/cutSummary").GetBinContent(1)
    das_nevents = ZHinv_datasets[name]['dbs_info']['nevents']
    print "% 8d, % 9d (%1.2f): %s" % (nevents, das_nevents, nevents/das_nevents, ZHinv_datasets[name]["name"])
    if not nevents > 0 :
      print "Empty tree for " + name
    else :
      tree.SetWeight(19.6e3*xs/das_nevents)
  eetrees[name] = tree

if not os.path.exists('plots/') :
  os.mkdir('plots')

c = stackUp(name="diLeptonMass",
    bins=50,
    xmin=91-25,
    xmax=91+25,
    trees=eetrees,
    variable="Mass",
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
    logY=True,
    ymin=1e-2,
    ymax=1e4,
    xtitle="p^{ll}_{T} [GeV]",
    ytitle="Events / 10 GeV")
cpt.Print("plots/diLeptonPt.root")
cpt.Print("plots/diLeptonPt.pdf")
