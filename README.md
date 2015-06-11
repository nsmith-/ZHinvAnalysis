Package Summary
---------------
This analysis code currently uses [FSA](https://github.com/nsmith-/FinalStateAnalysis/tree/ZHwork) to PAT-tuplize 8TeV data.
Some small additions were necessary, hence the [branch](https://github.com/uwcms/FinalStateAnalysis/compare/master...nsmith-:ZHwork).
PAT is then processed into FSA-style combinatoric TTree objects.
Output TTrees are skimmed using baseline selection described in AN2012-123 to produce `datasets/` folder.

### Package layout:
* `datasets` folder contains a single ROOT file for each dataset skim (`.gitignore`'d)
* `meta/ZHinv_datasets.py` will contain plot group and cross section information for each dataset

### Skim Process:
* Make metadata (described in `meta/README.md`)
* Run `run_skim.sh` to create the baseline selection tuple, will take a while
* Run `deduplicate.py` to remove any event double-counting from {Single,Double}Mu samples.

### Plots after baseline selection:
* Run `read_fsa_eventcount.py` to set up dataset weights
* Dilepton mass
* Dilepton pT
* (todo) Jet multiplicity
