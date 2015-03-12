#!/usr/bin/env python
import ROOT
# ROOT.gROOT.SetBatch(ROOT.kTRUE)
from stackUp import stackUp
import meta
import util
import os

if not os.path.exists('plots/') :
  os.mkdir('plots')

plotConfigs = []
plotConfigs.append({
    'name' : "diLeptonMass",
    'bins' : 50,
    'xmin' : 91-25,
    'xmax' : 91+25,
    'variable' : "Mass",
    'cut' : ['bestCandidate'],
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e6,
    'xtitle' : "M_{ll} [GeV]",
    'ytitle' : "Events / 1 GeV"
    })

plotConfigs.append({
    'name' : "diLeptonPt",
    'bins' : 50,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "Pt",
    'cut' : ['bestCandidate'],
    'logY' : True,
    'ymin' : 1e-2,
    'ymax' : 1e4,
    'xtitle' : "p^{ll}_{T} [GeV]",
    'ytitle' : "Events / 10 GeV"
    })

plotConfigs.append({
    'name' : "reducedMETBalance",
    'bins' : 25,
    'xmin' : 0,
    'xmax' : 5,
    'variable' : "reducedMET/Pt",
    'cut' : ['bestCandidate'],
    'logY' : True,
    'ymin' : 1e-2,
    'ymax' : 1e4,
    'xtitle' : "#slash{E}_{T}/p^{ll}_{T}",
    'ytitle' : "Events / 0.2"
    })

eetrees = util.getDatasetTrees("ee/Ntuple", meta.ZHinv_datasets)
mmtrees = util.getDatasetTrees("mm/Ntuple", meta.ZHinv_datasets)

canvases = {}
for config in plotConfigs :
    config['cut'].append('doubleEPass')
    config['name'] += '_ee'
    canvas = stackUp(trees=eetrees, **config)
    canvases[config['name']] = canvas
    canvas.Print("plots/%s.pdf" % config['name'])
    canvas.Print("plots/%s.root" % config['name'])

    config['cut'].pop()
    config['name'] = config['name'].replace('_ee','_mm')
    config['cut'].append('doubleMuPass')
    canvas = stackUp(trees=mmtrees, **config)
    canvases[config['name']] = canvas
    canvas.Print("plots/%s.pdf" % config['name'])
    canvas.Print("plots/%s.root" % config['name'])

