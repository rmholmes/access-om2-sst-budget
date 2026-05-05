# Accurately diagnosing mixed layer tracer budgets in ACCESS-OM2/MOM5

This repository contains methodology and analysis routines for accurately diagnosing mixed layer tracer budgets in the ACCESS-OM2 global numerical ocean model. The methods make use of new online diagnostics added to the MOM5 source code for this purpose, as described in the following paper,

Holmes and Malan, Accurately diagnosing mixed layer tracer budgets and marine heatwave drivers in ocean models (late draft as of 6/5/2026).

## Repository contents

Jupyter notebooks:
- `Theory_and_Diagnostics.ipynb` - this notebook contains a short overview of the theory and diagnostics. See the above paper for more details on the theory. This notebook contains no code (only used because github can't seem to display latex equations in the README.md). 
- `Mixed_Layer_Temperature_Budget.ipynb` - contains code to load in pre-computed budget diagnostics and analyse an event/time period of interest (start here if you are new).
- `MHW_example_analysis.ipynb` - a more detailed and complete notebook for the analysis of MHW events (including actual MHW threshold exceedance plots) used to generate the analysis of the 2017/2018 Tasman Sea and 2011 WA events in the above paper.
- `Offline_Online_Budget_Comparison.ipynb` - contains code to compare online with offline methods.
- `Testing_and_Checks.ipynb` - contains code to perform a range of checks used during development of the methods (e.g. budget closure checks, diagnostic checks etc.).
- `Process_Online_Budget.ipynb` - contains code to pre-compute grouped budget terms (for use in Mixed_Layer_Temperature_Budget.ipynb) from raw mixed-layer-binned MOM5 diagnostics. Note that this code is only for testing, use the script `spawn_process_online_budget.py` for production runs. However, this notebook also contains a few other bits of processing code (e.g. code to compute climatologies of standard variables).
- `Hourly_analysis.ipynb` - contains code to analyse a short simulation performed with hourly budget output to examine subdaily variability.
- `Mixed_Layer_Temperature_Budget_offline.ipynb` - old code used to compute offline budgets before the online diagnostics were available.
- `Mixed_Layer_Salinity_Budget.ipynb` - as for `Mixed_Layer_Temperature_Budget.ipynb` but for salinity (minimal work done on this so far, beyond checking that it works).

Other scripts:
- `spawn_process_online_budget.py`, `process_online_budget_year.sub`, `process_online_budget_year_salinity.sub` and `process_online_hatavg_budget_year.sub` - scripts for computing the grouped mixed layer tracer budgets a year at a time using parallel PBS jobs on NCI. One for salinity and one for temperature (just modify which script is used in `spawn_process_online_budget.py` to choose which one), and one for hat-averaged temperature budgets.
- `process_offline_daily_budget_month.sub` and `spawn_process_offline_daily_budget.py` - scripts for computing the grouped mixed layer temperature budget for daily *offline* data (requires daily resolution 3D heat budget outputs).
- `process_offline_monthly_budget_month.sub` and `spawn_process_offline_monthly_budget.py` - scripts for computing the grouped mixed layer temperature budget for monthly *offline* data (requires monthly resolution 3D heat budget outputs).

## Suggestions for new users

Start by looking through the `Theory_and_Diagnostics.ipynb` notebook to get a feel for how things work. Then have a look at the `Mixed_Layer_Temperature_Budget.ipynb` and modify it for your event (spatial region and time period) of interest. Also see `MHW_example_analysis.ipynb` for a more in-depth analysis of several MHW events.
