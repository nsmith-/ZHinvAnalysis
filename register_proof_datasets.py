#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
import meta

data_tier = 'full'
reRegister = False

ROOT.TProof.Open('workers=6')
# TProof::Open returns pointer to proof-lite and messes with pyroot's
# inability to call virtual base class members
# gProof is base class type, so no issues
proof = ROOT.gProof

for name, info in meta.ZHinv_datasets.iteritems() :
    proof_name = '_'.join([name, data_tier])
    if proof.GetDataSet(proof_name) == None or reRegister :
        shortname = info['matching_pat'].keys()[0]
        filelist = ROOT.TFileCollection(proof_name, proof_name, 'datasets/%s.ntuples.txt' % shortname)
        proof.RegisterDataSet(proof_name, filelist, 'OVnostagedcheck:')
