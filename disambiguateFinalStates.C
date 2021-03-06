#define disambiguateFinalStates_cxx

#include "disambiguateFinalStates.h"


void disambiguateFinalStates::Begin(TTree * /*tree*/)
{
}

void disambiguateFinalStates::SlaveBegin(TTree * /*tree*/)
{
  fBestCandidateEntryList = new TEntryList("bestCandidates", "Entry List of disambiguated combinatoric candidates");
  fOutput->Add(fBestCandidateEntryList);
}

Bool_t disambiguateFinalStates::Process(Long64_t entry)
{
  b_evt->GetEntry(entry);
  b_run->GetEntry(entry);

  if ( !(run == fCurrentRun && evt == fCurrentEvt) )
  {
    findBestEntry();
  }

  fCurrentRun = run;
  fCurrentEvt = evt;
  
  if ( fCutFormula && fCutFormula->EvalInstance() > 0. )
  {
    b_Mass->GetEntry(entry);
    Float_t discriminant = fabs(Mass-91.);
    fEntriesToCompare.push_back(entry);
    fEntryDiscriminants.push_back(discriminant);
  }

  if ( entry == fChain->GetEntries()-1 ) {
    findBestEntry();
  }

  return kTRUE;
}

void disambiguateFinalStates::SlaveTerminate()
{
  fBestCandidateEntryList->OptimizeStorage();
  // Pointer is owned by fOutput, dereference
  fBestCandidateEntryList = nullptr;
}

void disambiguateFinalStates::Terminate()
{
}

void disambiguateFinalStates::findBestEntry()
{
  Long64_t bestEntry = -1L;
  Float_t lowestDiscriminant = 1e100;
  for (size_t i=0; i<fEntriesToCompare.size(); ++i)
  {
    if ( lowestDiscriminant > fEntryDiscriminants[i] )
    {
      lowestDiscriminant = fEntryDiscriminants[i];
      bestEntry = fEntriesToCompare[i];
    }
  }

  if ( bestEntry > 0 )
  {
    fBestCandidateEntryList->Enter(bestEntry);
  }

  fEntriesToCompare.clear();
  fEntryDiscriminants.clear();
}
