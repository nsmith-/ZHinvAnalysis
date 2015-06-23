#!/usr/bin/env python
import os, pickle
import ROOT
ROOT.gROOT.SetBatch(True)
import meta
from stackUp import stackUp
from splitCanvas import splitCanvas
from muonEfficiency import buildMuonEfficiencyRescaleString
from meta.pileupReweight import pileupReweightStrings

def setProofChainWeight(shortname, cross_section, lumi) :
    with open("datasets/"+shortname+".das_eventcount.txt") as evtcount :
        ntuple_eventcount = int(evtcount.read())
    weight = lumi*cross_section/ntuple_eventcount
    proof.SetParameter('PROOF_ChainWeight', weight)
    print "Weight for dataset %s set to %f" % (shortname, weight)

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
                cuts += ['doubleETightPass']
            elif channel == 'mm' :
                cuts += meta.mcuts
                cuts += ['doubleMuZHinvPass']
            
            infostr = "Starting processing of channel %s for dataset %s" % (channel, shortname)
            print infostr
            print '-'*len(infostr)

            disambiguator = ROOT.disambiguateFinalStates()
            proof.Process(proof_path, disambiguator, '&&'.join(cuts))
            entryList = disambiguator.GetOutputList().FindObject('bestCandidates')
            entryList.SetName('%s_%s_preselection' % (shortname, channel))
            if os.path.exists('datasets/%s.duplicates.root' % shortname) :
                df = ROOT.TFile.Open('datasets/%s.duplicates.root' % shortname)
                duplicates = df.Get('%s_duplicate_entries' % shortname)
                entryList.Subtract(duplicates)
            entryLists.append(entryList)

            drawCut = ''
            if info['type'] == 'mc' :
                drawCut = pileupReweightStrings['%s_%s_reweight_hist' % (name, channel)]
                # MC pileup correction closure test
                # proof.DrawSelect(proof_path, 'nTruePU >> +%s_nTruePU_hist(60, 0, 60)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
                # hist = proof.GetOutputList().FindObject(hist_prefix+'_nTruePU_hist')
                # hist.Scale(1. / hist.Integral())
                # objectsToSave.append(hist)
                if channel == 'mm' :
                    drawCut += '*'+buildMuonEfficiencyRescaleString()

            print drawCut
            mass_string = 'Mass'
            if channel == 'mm' :
                mass_string = 'sqrt(pow(m1PtRochCor2012*cosh(m1EtaRochCor2012)+m2PtRochCor2012*cosh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012*sinh(m1EtaRochCor2012)+m2PtRochCor2012*sinh(m2EtaRochCor2012),2) - pow(m1PtRochCor2012,2) - pow(m2PtRochCor2012,2) - 2*m1PtRochCor2012*m2PtRochCor2012*cos(m1PhiRochCor2012-m2PhiRochCor2012))'
            proof.DrawSelect(proof_path, mass_string+' >> +%s_Mass_hist(100, 40, 250)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_Mass_hist'))
            proof.DrawSelect(proof_path, 'Pt >> +%s_Pt_hist(100, 0, 500)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_Pt_hist'))
            proof.DrawSelect(proof_path, 'reducedMET >> +%s_reducedMET_hist(100, 0, 500)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_reducedMET_hist'))
            proof.DrawSelect(proof_path, 'type1_pfMetEt >> +%s_pfMetEt_hist(100, 0, 500)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_pfMetEt_hist'))
            proof.DrawSelect(proof_path, 'nvtx >> +%s_nvtx_hist(50, 1, 50)'%hist_prefix, drawCut, 'goff', -1, 0, entryList)
            objectsToSave.append(proof.GetOutputList().FindObject(hist_prefix+'_nvtx_hist'))

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

plotConfigs.append({
    'name' : "pfMetEt",
    'bins' : 100,
    'xmin' : 0,
    'xmax' : 500,
    'variable' : "type1_pfMetEt",
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "PF #slash{E}_{T}",
    'ytitle' : "Events / 5 GeV"
    })

plotConfigs.append({
    'name' : "nvtx",
    'bins' : 50,
    'xmin' : 1,
    'xmax' : 50,
    'variable' : "nvtx",
    'logY' : True,
    'ymin' : 1e-1,
    'ymax' : 1e7,
    'xtitle' : "# PU Vertices",
    'ytitle' : "Events / PU Bin"
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


