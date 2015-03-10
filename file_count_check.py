#!/usr/bin/env python

def das_count(dataset_name) :
    from meta.das_query import das_query
    result = das_query('dataset dataset=%s |grep dataset.nfiles' % dataset_name)
    try :
        dataset = result['data'][0]['dataset']
        for row in dataset :
            if 'nfiles' in row :
                return row['nfiles']
        return 0
    except KeyError :
        print "Couldn't find key in json while finding DAS count for: %s" % dataset_name
        import json
        print json.dumps(result, indent=4)
        raise

def pat_count(shortname) :
    from get_missing_event_count import get_pat_file_dict
    pat_dict = get_pat_file_dict(shortname)
    pat_count = 0
    for infiles in pat_dict.itervalues() :
        pat_count += len(infiles)
    return pat_count

if __name__ == '__main__' :
    import sys, json
    longnamemap = json.load(open('meta/shortname_dataset_map.json'))
    with open('meta/sample_shortnames.txt') as f :
        for line in f :
            shortname = line.strip()
            longname = longnamemap[shortname]['das_name']
            patcount = pat_count(shortname)
            dascount = das_count(longname)
            print "% 6d, % 6d (%3.1f%%): %s" % (patcount, dascount, patcount*100./dascount, shortname)
