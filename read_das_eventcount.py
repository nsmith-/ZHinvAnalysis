#!/usr/bin/env python

def get_dataset_files(dataset_name) :
  from meta.das_query import das_query
  files = das_query('file dataset=%s |grep file.name,file.nevents,file.dataset' % dataset_name)
  dataset_files = []
  for row in files['data'] :
    if 'file' in row :
      for result in row['file'] :
        if len(result) == 3 :
          dataset_files.append(result)
  return dataset_files

def get_pat_file_dict(shortname) :
  pat_files = {}
  with open('datasets/%s.pattuples.txt' % shortname) as file :
    for line in file :
      args = line.split()
      ntuple_outfile = ''
      pat_infiles = []
      for arg in args :
        if 'inputFiles' in arg :
          pat_infiles = arg.strip("'").replace('inputFiles=','').split(',')
        elif 'outputFile' in arg :
          ntuple_outfile = arg.strip("'").replace('outputFile=','')
      full_ntuple_outfile = 'root://cmsxrootd.hep.wisc.edu//store/user/nsmith/ZHinvNtuples/%s/%s' % (shortname, ntuple_outfile)
      pat_files[full_ntuple_outfile] = pat_infiles
  return pat_files

def get_das_event_count(shortname) :
  pat_files = get_pat_file_dict(shortname)
  new_pat_files = {}
  with open('datasets/%s.ntuples.txt' % shortname) as ntuples_file :
    for line in ntuples_file :
      ntuple_filename = line.strip()
      if ntuple_filename in pat_files :
        new_pat_files[ntuple_filename] = pat_files[ntuple_filename]

  das_files = []
  for ntuple_name, pat_names in new_pat_files.iteritems() :
    for pat_name in pat_names :
      token = 'patTuple_cfg-'
      das_filename = pat_name[pat_name.find(token)+len(token):]
      das_files.append(das_filename)
  if len(das_files) == 0 :
    return 0

  import json
  longname = json.load(open('meta/shortname_dataset_map.json'))[shortname]['das_name']
  dataset_files = get_dataset_files(longname)
  das_events = 0
  for dataset_file in dataset_files :
    filename = dataset_file['name'].split('/')[-1]
    if filename in das_files :
      das_events += dataset_file['nevents']

  return das_events

if __name__ == '__main__' :
  import sys
  print get_das_event_count(sys.argv[1])
