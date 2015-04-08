#!/usr/bin/env python
from ZHinv_datasets import ZHinv_datasets

dataset_xsec = []
for name, info in ZHinv_datasets.iteritems() :
    if info['type'] == 'mc' :
        dataset_xsec.append((info['name'], info['cross_section']))

dataset_xsec.sort()

print "{name:^100} | {xsec:^20}".format(name='Dataset Name', xsec='Cross Section [pb]')
print "-"*123
for tup in dataset_xsec :
    print "{name:<100} | {xsec:^20.2f}".format(name=tup[0], xsec=tup[1])
