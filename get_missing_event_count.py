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

def get_missing_event_count(shortname) :
  pat_files = get_pat_file_dict(shortname)
  with open('datasets/%s.ntuples.txt' % shortname) as ntuples_file :
    for line in ntuples_file :
      ntuple_filename = line.strip()
      if ntuple_filename in pat_files :
        pat_files.pop(ntuple_filename)
      else :
        print "%s not in the ntuplizer!!" % ntuple_filename

  missing_das_files = []
  for ntuple_name, pat_names in pat_files.iteritems() :
    for pat_name in pat_names :
      token = 'patTuple_cfg-'
      das_filename = pat_name[pat_name.find(token)+len(token):]
      missing_das_files.append(das_filename)
  if len(missing_das_files) == 0 :
    return 0

  import json
  longname = json.load(open('meta/shortname_dataset_map.json'))[shortname]['das_name']
  dataset_files = get_dataset_files(longname)
  missing_events = 0
  for dataset_file in dataset_files :
    filename = dataset_file['name'].split('/')[-1]
    if filename in missing_das_files :
      missing_events += dataset_file['nevents']

  return missing_events

if __name__ == '__main__' :
  import sys
  print get_missing_event_count(sys.argv[1])
