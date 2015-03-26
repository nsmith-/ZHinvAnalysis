#!/usr/bin/env python
import ROOT
import meta

ROOT.TProof.Open('workers=4')
# TProof::Open return proof-lite and messes with pyroot's
# inability to call virtual base class members
# gProof is base class type, so no issues
proof = ROOT.gProof

data_tier = 'full'

for name, info in meta.ZHinv_datasets.iteritems() :
    proof_name = '_'.join([name, data_tier])
    if proof.GetDataSet(proof_name) == None :
        shortname = info['matching_pat'].keys()[0]
        filelist = ROOT.TFileCollection(proof_name, proof_name, 'datasets/%s.ntuples.txt' % shortname)
        proof.RegisterDataSet(proof_name, filelist, 'OVnostagedcheck:')
