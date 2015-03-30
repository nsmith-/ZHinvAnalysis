#!/usr/bin/env python
import os
import ROOT
ROOT.gROOT.SetBatch(True)
import meta
from stackUp import stackUp
from splitCanvas import splitCanvas

if not os.path.exists('preselection_plots.root') :
    data_tier = 'full'
    ROOT.TProof.Open('workers=12')
    proof = ROOT.gProof

    hists =[]
    for name, info in meta.ZHinv_datasets.iteritems() :
        proof_name = '_'.join([name, data_tier])
        if info['type'] == 'mc' :
            shortname = info['matching_pat'].keys()[0]
            with open("datasets/"+shortname+".ntuple_eventcount.txt") as evtcount :
                ntuple_eventcount = int(evtcount.read())
            lumi = 19.238e3
            xs = info['cross_section']
            weight = lumi*xs/ntuple_eventcount
            proof.SetParameter('PROOF_ChainWeight', weight)
        cuts = list(meta.ecuts)
        if info['type'] == 'data' :
            cuts += ['doubleETightPass']
        proof.DrawSelect(proof_name+'#/ee/final/Ntuple', 'Mass >> +%s_Mass_hist(100, 40, 250)'%name, '&&'.join(cuts), 'goff')
        hists.append(proof.GetOutputList().FindObject(name+'_Mass_hist'))
        proof.DrawSelect(proof_name+'#/ee/final/Ntuple', 'Pt >> +%s_Pt_hist(100, 0, 500)'%name, '&&'.join(cuts), 'goff')
        hists.append(proof.GetOutputList().FindObject(name+'_Pt_hist'))
        proof.DrawSelect(proof_name+'#/ee/final/Ntuple', 'reducedMET >> +%s_reducedMET_hist(100, 0, 500)'%name, '&&'.join(cuts), 'goff')
        hists.append(proof.GetOutputList().FindObject(name+'_reducedMET_hist'))

    out = ROOT.TFile('preselection_plots.root', 'recreate')
    out.cd()
    for hist in hists :
        hist.Write()
    out.Close()

plotConfigs = []
plotConfigs.append({
    'name' : "Mass",
    'bins' : 100,
    'xmin' : 40,
    'xmax' : 250,
    'variable' : "Mass",
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "M_{ll} [GeV]",
    'ytitle' : "Events / 2.1 GeV"
    })

plotConfigs.append({
    'name' : "Pt",
    'bins' : 100,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "Pt",
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "p^{ll}_{T} [GeV]",
    'ytitle' : "Events / 5 GeV"
    })

plotConfigs.append({
    'name' : "reducedMET",
    'bins' : 100,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "reducedMET",
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "Reduced #slash{E}_{T}",
    'ytitle' : "Events / 5 GeV"
    })

plotfile = ROOT.TFile('preselection_plots.root')

if not os.path.exists('plots/preselection') :
  os.mkdir('plots/preselection')

canvases = {}
for config in plotConfigs :
    canvas = splitCanvas(stackUp(plotfile=plotfile, **config))
    canvases[config['name']] = canvas
    canvas.Print("plots/preselection/%s.pdf" % config['name'])
    canvas.Print("plots/preselection/%s.root" % config['name'])


