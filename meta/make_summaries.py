#!/bin/env python
import json
import re
import os
from ZHinv_datasets import ZHinv_datasets

pat_to_tuplize = {}

sample_summary = "%50s %20s %100s %30s\n" % ('data8TeV.py name', 'username', 'DAS Path', 'Campaign')
sample_summary += "-"*len(sample_summary)+"\n"

# Handy for shell scripts on ntuples
sample_shortnames = []

# Occasionally need to map tuple names back to our dataset definition
shortname_dataset_map = {}

with open('ZHinv_datasets.json') as datafile :
  ZHinv_datasets = json.load(datafile)
  for name, info in ZHinv_datasets.iteritems() :
    if len(info['matching_pat']) > 1 :
      print "More than one matching PAT tuple for %s" % name
    else :
      key = info['matching_pat'].keys()[0]
      sample_shortnames.append(key)
      shortname_dataset_map[key] = { 'ZHinv_datasets_name' : name, 'das_name' : info['name'] }
      info['matching_pat'][key]['location'] = info['matching_pat'][key]['locations'][0]
      location = info['matching_pat'][key]['location']['dir']
      pat_to_tuplize.update({key : location})
      p = re.compile('/hdfs/store/user/([^/]*)/(.*)/([^/]*)$')
      m = p.match(location)
      if m :
        (user, dasset, campaign) = m.groups()
        sample_summary += "%50s %20s %100s %30s\n" % (key, user, "/"+dasset, campaign)
      else :
        sample_summary += location+"\n"
      info['matching_pat'][key].pop('locations')

with open('samples_used.txt', 'w') as out :
  out.write(sample_summary)

with open('tuple_dirs.json', 'w') as out :
  json.dump(pat_to_tuplize, out, indent=4)

with open('sample_shortnames.txt', 'w') as out :
  out.write("\n".join(sample_shortnames))

with open('shortname_dataset_map.json', 'w') as out :
  json.dump(shortname_dataset_map, out, indent=4)
