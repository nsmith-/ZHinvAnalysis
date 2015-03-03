Sequence used to produce metadata:

* `match_PAT.py` produces `ZHinv_datasets_toedit.json`
* This is edited to remove duplicate data locations, renamed `ZHinv_datasets.json` (versioned for now)
* `make_summaries.py` uses the previous file to make some useful information:
  * `samples_used.txt` Pretty-formatted summary of PAT used
  * `tuple_dirs.json` File to provide to FSA `submit_job.py` tool for PAT locations
  * `sample_shortnames.txt` Convinient for shell scripts, NTuples are in `/hdfs/store/user/nsmith/ZHinvNtuples/<shortname/`
