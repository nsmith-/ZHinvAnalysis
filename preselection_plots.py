#!/usr/bin/env python
import os
import ROOT
ROOT.gROOT.SetBatch(True)
import meta
from stackUp import stackUp
from splitCanvas import splitCanvas

def setProofChainWeight(shortname, cross_section, lumi) :
    with open("datasets/"+shortname+".das_eventcount.txt") as evtcount :
        ntuple_eventcount = int(evtcount.read())
    weight = lumi*cross_section/ntuple_eventcount
    proof.SetParameter('PROOF_ChainWeight', weight)
    print "Weight for dataset %s = %f" % (shortname, weight)

channels = ['ee', 'mm']

if not os.path.exists('preselection_plots.root') :
    data_tier = 'full'
    ROOT.TProof.Open('workers=8')
    proof = ROOT.gProof
    proof.Load('disambiguateFinalStates.C+')

    lumis = { 'ee' : 19.238e3, 'mm' : 19.762e3 }
    objectsToSave =[]
    entryLists = []

    for name, info in meta.ZHinv_datasets.iteritems() :
        shortname = info['matching_pat'].keys()[0]
        proof_name = '_'.join([name, data_tier])
        
        for channel in channels :
            proof.DeleteParameters('PROOF_ChainWeight')
            if info['type'] == 'mc' :
                setProofChainWeight(shortname, info['cross_section'], lumis[channel])
            proof_path = '%s#/%s/final/Ntuple' % (proof_name, channel)
            hist_prefix = '_'.join([proof_name, channel])
            
            cuts = []
            if channel == 'ee' :
                cuts += meta.ecuts
                if info['type'] == 'data' :
                    cuts += ['doubleETightPass']
            elif channel == 'mm' :
                cuts += meta.mcuts
                if info['type'] == 'data' :
                    cuts += ['doubleMuZHinvPass']

            disambiguator = ROOT.disambiguateFinalStates()
            proof.Process(proof_path, disambiguator, '&&'.join(cuts))
            entryList = disambiguator.GetOutputList().FindObject('bestCandidates')
            entryList.SetName('%s_%s_preselection' % (shortname, channel))
            if os.path.exists('datasets/%s.duplicates.root' % shortname) :
                df = ROOT.TFile.Open('datasets/%s.duplicates.root' % shortname)
                duplicates = df.Get('%s_duplicate_entries' % shortname)
                entryList.Subtract(duplicates)
            entryLists.append(entryList)

            proof.DrawSelect(proof_path, 'Mass >> +%s_Mass_hist(100, 40, 250)'%hist_prefix, '', 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_Mass_hist'))
            proof.DrawSelect(proof_path, 'Pt >> +%s_Pt_hist(100, 0, 500)'%hist_prefix, '', 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_Pt_hist'))
            proof.DrawSelect(proof_path, 'reducedMET >> +%s_reducedMET_hist(100, 0, 500)'%hist_prefix, '', 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_reducedMET_hist'))

    out = ROOT.TFile('preselection_plots.root', 'recreate')
    out.cd()
    for obj in objectsToSave :
        obj.Write()
    for elist in entryLists :
        elist.Write()
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

def makeSaveDir(path) :
    if not os.path.exists(path) :
        os.makedirs(path)
    return path

for config in plotConfigs :
    for channel in channels :
        saveDir = makeSaveDir('plots/%s/preselection/'%channel)
        canvas = splitCanvas(stackUp(plotfile=plotfile, channel=channel, proof_prefix='full', **config))
        canvas.Print(saveDir+config['name']+'.pdf')
        canvas.Print(saveDir+config['name']+'.root')


