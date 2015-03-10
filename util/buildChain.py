import ROOT

def buildChain(fileListName, ntupleName) :
  chain = ROOT.TChain(ntupleName)
  with open(fileListName) as fileList :
    nfiles = 0
    for fileName in fileList :
      chain.Add(fileName.strip())
      nfiles += 1
      if nfiles > 40 :
        break
  return chain


