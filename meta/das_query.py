#!/usr/bin/env python
import json

def das_query ( query ) :
  '''
  returns json object with result of query
  '''
  import subprocess
  cmd = ['das_client.py',
      '--limit=0',
      '--format=json',
      '--query="%s"' % query]
  output = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE).stdout
  result = json.load(output)
  if result['status'] != 'ok' :
    raise Exception('DAS query returned result status %s' % result['status'])
  return result

if __name__ == '__main__' :
  import sys
  result = das_query(sys.argv[1])
  print json.dumps(result, indent=4)
