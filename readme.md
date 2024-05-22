# Extend & Bias of MHC

Little code for calcul and osberve Bias with XTC, between langage and target, with an extension of MHC. 

# Execution

You have 2 differents parts : 

## `run_calcul.py` 

Allows you to create cases (from templates and IDENT (target)) and calculate predictions with XTC.
In the code, these two parts have a `force` argument : create cases and make prediction are made if cases_final.csv and predictions.csv doesn't exist.
But, if you want to "refresh", you need to put `force=True`. In this repos, cases_final and predictions are already done ! 

## `run_results.py`

When cases_final.csv and predictions.csv are made, this code create result csv and graph

## Device for execution

I don't use CUDA, so if you want / can use it, you need to add it in the code

# Requierement

* `pandas==2.0.3`
* `numpy==1.25.2`
* `coloralf==0.3`
* `transformers==4.39.3`
* `tqdm==4.66.1`
* `seaborn==0.13.2`
* `matplotlib==3.8.2`
* `sklearn==1.3.2`

