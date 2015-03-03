Sequence used to produce metadata:

* `match_PAT.py` produces `ZHinv_datasets_toedit.json`
* This is edited to remove duplicate data locations, renamed `ZHinv_datasets.json` (versioned for now)
* `make_summaries.py` uses the previous file to make some useful information:
  * `samples_used.txt`
  * `tuple_dirs.json`
  * `sample_shortnames.txt`
