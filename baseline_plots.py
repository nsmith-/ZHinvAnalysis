#!/usr/bin/env python
import ROOT
# ROOT.gROOT.SetBatch(ROOT.kTRUE)
from stackUp import stackUp
from splitCanvas import splitCanvas
import meta
import util
import os

for channel in ['ee', 'mm'] :
    if not os.path.exists('plots/%s/baseline' % channel) :
        os.makedirs('plots/%s/baseline' % channel)

plotConfigs = []
plotConfigs.append({
    'name' : "diLeptonMass",
    'bins' : 50,
    'xmin' : 91-25,
    'xmax' : 91+25,
    'variable' : "Mass",
    'cut' : [],
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
    'cut' : [],
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
    'cut' : [],
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
    config['name'] += '_ee'
    canvas = splitCanvas(stackUp(trees=eetrees, **config))
    canvases[config['name']] = canvas
    canvas.Print("plots/ee/baseline/%s.pdf" % config['name'])
    canvas.Print("plots/ee/baseline/%s.root" % config['name'])

    config['name'] = config['name'].replace('_ee','_mm')
    canvas = splitCanvas(stackUp(trees=mmtrees, **config))
    canvases[config['name']] = canvas
    canvas.Print("plots/mm/baseline/%s.pdf" % config['name'])
    canvas.Print("plots/mm/baseline/%s.root" % config['name'])

