#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import meta
from stackUp import stackUp
import util

plotConfigs = []
plotConfigs.append({
    'name' : "diLeptonMass_preselection",
    'bins' : 100,
    'xmin' : 40,
    'xmax' : 250,
    'variable' : "Mass",
    'cut' : [],
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "M_{ll} [GeV]",
    'ytitle' : "Events / 2.1 GeV"
    })

eetrees = util.getDatasetTrees("ee/final/Ntuple", meta.ZHinv_datasets)

canvases = {}
for config in plotConfigs :
    config['cut'].append('doubleEPass')
    config['cut'].extend(meta.ecuts)
    config['name'] += '_ee'
    canvas = stackUp(trees=eetrees, **config)
    canvases[config['name']] = canvas
    canvas.Print("plots/%s.pdf" % config['name'])
    canvas.Print("plots/%s.root" % config['name'])


