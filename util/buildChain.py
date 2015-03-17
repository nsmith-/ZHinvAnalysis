import ROOT

def buildChain(fileName, ntupleName, maxFiles=0) :
  chain = ROOT.TChain(ntupleName)
  if '.txt' in fileName :
    with open(fileName) as fileList :
      nfiles = 0
      for f in fileList :
        chain.Add(f.strip())
        nfiles += 1
        if maxFiles > 0 and nfiles > maxFiles :
          break
  elif '.root' in fileName :
    chain.Add(fileName)
  else :
    raise IOError( "I don't know what to do with %s" % fileName)
  return chain



