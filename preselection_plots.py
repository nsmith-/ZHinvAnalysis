#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
import meta

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
    cuts = meta.ecuts
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
