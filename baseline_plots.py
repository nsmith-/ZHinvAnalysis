#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
from stackUp import stackUp
from splitCanvas import splitCanvas
import meta
import util
import os

for channel in ['ee', 'mm'] :
    if not os.path.exists('plots/%s/baseline' % channel) :
        os.makedirs('plots/%s/baseline' % channel)

mass_string = 'sqrt(pow(m1PtRochCor2012*cosh(m1EtaRochCor2012)+m2PtRochCor2012*cosh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012*sinh(m1EtaRochCor2012)+m2PtRochCor2012*sinh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012,2) - pow(m2PtRochCor2012,2) - 2*m1PtRochCor2012*m2PtRochCor2012*cos(m1PhiRochCor2012-m2PhiRochCor2012))'

plotConfigs = []
plotConfigs.append({
    'name' : "eventCount",
    'bins' : 1,
    'xmin' : 91-10,
    'xmax' : 91+10,
    'variable' : mass_string,
    'cut' : [],
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "M_{ll} [GeV]",
    'ytitle' : "Events"
    })

plotConfigs.append({
    'name' : "diLeptonMass",
    'bins' : 10,
    'xmin' : 91-10,
    'xmax' : 91+10,
    'variable' : "Mass",
    'cut' : [],
    'logY' : False,
    'ymin' : 0.0001,
    'ymax' : 50,
    'xtitle' : "M_{ll} [GeV]",
    'ytitle' : "Events / 5 GeV"
    })

plotConfigs.append({
    'name' : "diLeptonPt",
    'bins' : 10,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "Pt",
    'cut' : [],
    'logY' : False,
    'ymin' : 0.0001,
    'ymax' : 60,
    'xtitle' : "p^{ll}_{T} [GeV]",
    'ytitle' : "Events / 50 GeV"
    })
plotConfigs.append({
    'name' : "METBalance",
    'bins' : 25,
    'xmin' : 0,
    'xmax' : 5,
    'variable' : "type1_pfMetEt /Pt",
    'cut' : [],
    'logY' : False,
    'ymin' : 0.0001,
    'ymax' : 80,
    'xtitle' : "#slash{E}_{T}/p^{ll}_{T}",
    'ytitle' : "Events / 0.2"
    })

plotConfigs.append({
    'name' : "mvaMET",
    'bins' : 50,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "mva_metEt",
    'cut' : [],
    'logY' : True,
    'ymin' : 1e-2,
    'ymax' : 1e4,
    'xtitle' : "MVA #slash{E}_{T}",
    'ytitle' : "Events / 10 GeV"
    })

plotConfigs.append({
    'name' : "MET",
    'bins' : 50,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "type1_pfMetEt",
    'cut' : [],
    'logY' : True,
    'ymin' : 1e-2,
    'ymax' : 1e4,
    'xtitle' : "#slash{E}_{T}",
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

plotConfigs.append({
    'name' : "reducedMET",
    'bins' : 50,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "reducedMET",
    'cut' : [],
    'logY' : True,
    'ymin' : 1e-2,
    'ymax' : 1e4,
    'xtitle' : "#slash{E}_{T}",
    'ytitle' : "Events / 10 GeV"
    })

plotConfigs.append({
    'name' : "MTtoMET",
    'bins' : 20,
    'xmin' : 0,
    'xmax' : 1000,
    'variable' : "mtToMET",
    'cut' : [],
    'logY' : False,
    'ymin' : 0.0001,
    'ymax' : 40,
    'xtitle' : "m_{T}",
    'ytitle' : "Events / 50 GeV"
    })

plotConfigs.append({
    'name' : "deltaPhi",
    'bins' : 10,
    'xmin' : 0,
    'xmax' : 3.14159,
    'variable' : "e1_e2_ToMETDPhi_Ty1",
    'cut' : [],
    'logY' : False,
    'ymin' : 0.0001,
    'ymax' : 50,
    'xtitle' : "#Delta#phi",
    'ytitle' : "Events / .1 rad"
    })

mmtrees = util.getDatasetTrees("mm/Ntuple", meta.ZHinv_datasets)

canvases = {}
for config in plotConfigs :
    config['name'] += '_mm'
    config['variable'] = config['variable'].replace('e1_e2','m1_m2')
    canvas = splitCanvas(stackUp(trees=mmtrees, **config))
    canvases[config['name']] = canvas
    canvas.Print("plots/mm/baseline/%s.pdf" % config['name'])
    canvas.Print("plots/mm/baseline/%s.root" % config['name'])

