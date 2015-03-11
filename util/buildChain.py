import ROOT

def buildChain(fileListName, ntupleName, maxFiles=0) :
  chain = ROOT.TChain(ntupleName)
  with open(fileListName) as fileList :
    nfiles = 0
    for fileName in fileList :
      chain.Add(fileName.strip())
      nfiles += 1
      if maxFiles > 0 and nfiles > maxFiles :
        break
  return chain


