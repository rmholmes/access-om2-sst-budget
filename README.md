# Accurately diagnosing mixed layer tracer budgets in ACCESS-OM2/MOM5

This repository contains methodology and analysis routines for accurately diagnosing mixed layer tracer budgets in the ACCESS-OM2 global numerical ocean model. The methods make use of new online diagnostics added to the MOM5 source code for this purpose, as described in the following paper,

Holmes, Malan and Bladwell, Accurately diagnosing mixed layer tracer budgets in a global ocean model, in preparation.

## Repository contents

This README 

Jupyter notebooks:
- `Theory_and_Diagnostics.ipynb` - this notebook contains a short overview of the theory and diagnostics. See the above paper for more details on the theory. This notebook contains no code (only used because github can't seem to display latex equations in the README.md).
- `Mixed_Layer_Temperature_Budget.ipynb` - contains code to load in pre-computed budget diagnostics and analyse an event/time period of interest (start here if you are new).
- `Offline_Online_Budget_Comparison.ipynb` - contains code to compare online with offline methods.
- `Testing_and_Checks.ipynb` - contains code to perform a range of checks used during development of the methods (e.g. budget closure checks, diagnostic checks etc.).
- `Process_Online_Budget.ipynb` - contains code to pre-compute grouped budget terms (for use in Mixed_Layer_Temperature_Budget.ipynb) from raw mixed-layer-binned MOM5 diagnostics. Note that this code is only for testing, use the script `spawn_process_online_budget.py` for production runs. However, this notebook also contains a few other bits of processing code (e.g. code to compute climatologies of standard variables).
- `Mixed_Layer_Temperature_Budget_offline.ipynb` - old code used to compute offline budgets before the online diagnostics were available.
- `Mixed_Layer_Salinity_Budget.ipynb` - as for `Mixed_Layer_Temperature_Budget.ipynb` but for salinity (minimal work done on this so far, beyond checking that it works).

Other scripts:
- `spawn_process_online_budget.py` and `process_online_budget_year.sub` - scripts for computing the grouped mixed layer tracer budgets a year at a time using parallel PBS jobs on NCI.
