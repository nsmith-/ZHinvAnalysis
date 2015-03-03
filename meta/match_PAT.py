#!/bin/env python
import json
import re
import os
from ZHinv_datasets import ZHinv_datasets

def match_pat ( patfilename ) :
  with open(patfilename) as patfile :
    pat = json.load(patfile)
    for name, info in ZHinv_datasets.iteritems() :
      matching_pat = {}
      # Search for matching DAS names in PAT tuples
      compare_left = info['name']
      for pat_name, pat_info in pat.iteritems() :
        if type(pat_info) is dict :
          compare_right = pat_info['datadef']['datasetpath']
          if compare_left == compare_right :
            matching_pat.update({pat_name : pat_info})
            if len(pat_info['locations']) > 1 :
              print "Dataset %50s has more than one matching PAT location in %s" % (name, patfilename)
      # merge with existing pat
      matching_pat.update(info.get('matching_pat',{}))
      info['matching_pat'] = matching_pat
      if len(matching_pat) == 0 :
        print "Dataset %50s has no matching PAT in %s" % (name, patfilename)
      elif len(matching_pat) > 1 :
        print "Dataset %50s has more than one matching PAT definition in %s" % (name, patfilename)

# See http://www.hep.wisc.edu/~nsmith/userPAT.html
# Made with `findUserTuples.py mcepeda,nsmith,dntaylor,belknap,taroni,tperry,aglevine`
# using https://github.com/uwcms/FinalStateAnalysis/blob/UpdatedDatadefsFeb15/MetaData/tuples/findUserTuples.py
match_pat(os.path.expanduser('~nsmith/public_html/pat_datadefs.json'))

with open('ZHinv_datasets_toedit.json','w') as outfile :
  json.dump(ZHinv_datasets, outfile, indent=4)

