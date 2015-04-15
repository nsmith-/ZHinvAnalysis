#!/usr/bin/env python
import os
import ROOT
ROOT.gROOT.SetBatch(True)
import meta

channels = ['ee', 'mm']
data_tier = 'full'

if not os.path.exists('mcPileup.root') :
    ROOT.TProof.Open('workers=8')
    proof = ROOT.gProof

    objectsToSave =[]

    for channel in channels :
        for name, info in meta.ZHinv_datasets.iteritems() :
            if info['type'] != 'mc' :
                continue
            proof_name = '_'.join([name, data_tier])
            proof_path = '%s#/%s/final/Ntuple' % (proof_name, channel)

            histname = '_'.join([name, data_tier, channel, 'nTruePU', 'hist'])
            proof.DrawSelect(proof_path, 'nTruePU >> +%s(60, 0, 60)'%histname, 'idx==0', 'goff')
            hist = proof.GetOutputList().FindObject(histname)
            hist.Sumw2()
            hist.Scale( 1. / hist.Integral() )
            objectsToSave.append(hist)

    out = ROOT.TFile('mcPileup.root', 'recreate')
    out.cd()
    for obj in objectsToSave :
        obj.Write()
    out.Close()

# From https://twiki.cern.ch/twiki/bin/view/CMS/Pileup_MC_Gen_Scenarios
PUS10_hist = ROOT.TH1F('PU_S10', 'Nominal PU_S10 scenario', 60, 0, 60)
PUS10_values = [
        2.560E-06,5.239E-06,1.420E-05,5.005E-05,1.001E-04,2.705E-04,1.999E-03,6.097E-03,1.046E-02,1.383E-02,
        1.685E-02,2.055E-02,2.572E-02,3.262E-02,4.121E-02,4.977E-02,5.539E-02,5.725E-02,5.607E-02,5.312E-02,
        5.008E-02,4.763E-02,4.558E-02,4.363E-02,4.159E-02,3.933E-02,3.681E-02,3.406E-02,3.116E-02,2.818E-02,
        2.519E-02,2.226E-02,1.946E-02,1.682E-02,1.437E-02,1.215E-02,1.016E-02,8.400E-03,6.873E-03,5.564E-03,
        4.457E-03,3.533E-03,2.772E-03,2.154E-03,1.656E-03,1.261E-03,9.513E-04,7.107E-04,5.259E-04,3.856E-04,
        2.801E-04,2.017E-04,1.439E-04,1.017E-04,7.126E-05,4.948E-05,3.405E-05,2.322E-05,1.570E-05,5.005E-06]
for i in range(60) :
    PUS10_hist.SetBinContent(i+1, PUS10_values[i])
PUS10_hist.SetLineWidth(2)

def makeSaveDir(path) :
    if not os.path.exists(path) :
        os.makedirs(path)
    return path
makeSaveDir('plots/pileup')

mcPileupFile = ROOT.TFile.Open('mcPileup.root')

for channel in channels :
    hname = 'all_mc_pileups_'+channel
    c = ROOT.TCanvas(hname+'_canvas', '')
    stack = ROOT.THStack(hname+'_stack', '')
    i=20
    for name, info in meta.ZHinv_datasets.iteritems() :
        if info['type'] != 'mc' :
            continue
        histname = '_'.join([name, data_tier, channel, 'nTruePU', 'hist'])
        hist = mcPileupFile.Get(histname)
        hist.SetLineColor(i)
        i+=1
        stack.Add(hist)
    stack.Draw('nostack')
    stack.GetXaxis().SetTitle('True MC Pileup Interactions')
    stack.GetYaxis().SetTitle('Normalized')
    PUS10_hist.Draw('same')
    c.Print('plots/pileup/%s.root' % hname)
    c.Print('plots/pileup/%s.pdf' % hname)

c = ROOT.TCanvas('data_pileups', '')
stack = ROOT.THStack('data_pileups_stack', '')
files = {
    'ee' : 'meta/DoubleElectron.pileup.root',
    'mm' : 'meta/Muon.pileup.root'
    }
colors = {
    'ee' : ROOT.kBlue,
    'mm' : ROOT.kGreen
    }
for channel in channels :
    pileupFile = ROOT.TFile.Open(files[channel])
    pileupHist = pileupFile.Get('pileup')
    pileupHist.SetNameTitle('pileup_%s'%channel, '%s channel'%channel)
    pileupHist.Scale(1./pileupHist.Integral())
    pileupHist.SetLineColor(colors[channel])
    stack.Add(pileupHist)

stack.Add(PUS10_hist)

stack.Draw('nostack')
c.BuildLegend()
c.Print('plots/pileup/data_pileups.root')
c.Print('plots/pileup/data_pileups.pdf')

# ok, this is probably the stupidest thing ever
# but it works for now
def reweightString(histogram) :
    reweightBins = []
    for i in range(60) :
        pu_lessthan = histogram.GetBinLowEdge(i+2)
        pu_weight = histogram.GetBinContent(i+1)
        reweightBins.append('(nTruePU<%f)?%f' % (pu_lessthan, pu_weight))
    reweightBins.append('1.')
    return '(%s)' % ':'.join(reweightBins)

print "pileupReweightStrings = {}"
for channel in channels :
    pileupHist = stack.GetHists().FindObject('pileup_%s' % channel)
    for name, info in meta.ZHinv_datasets.iteritems() :
        if info['type'] != 'mc' :
            continue
        reweightHistName = '%s_%s_reweight_hist' % (name, channel)
        reweightHist = pileupHist.Clone(reweightHistName)
        mcHistName = '_'.join([name, data_tier, channel, 'nTruePU', 'hist'])
        mcHist = mcPileupFile.Get(mcHistName)
        reweightHist.Divide(mcHist)
        print "pileupReweightStrings['%s'] = '(%s)'" % (reweightHistName, reweightString(reweightHist))
    reweightHistName = 'nominal_%s_reweight_hist' % channel
    reweightHist = pileupHist.Clone(reweightHistName)
    reweightHist.Divide(PUS10_hist)
    print "pileupReweightStrings['%s'] = '(%s)'" % (reweightHistName, reweightString(reweightHist))
