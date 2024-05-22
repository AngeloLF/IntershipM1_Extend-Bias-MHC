from transformers import pipeline
import os
import pandas as pd
import csv
import coloralf as c
import numpy as np
from tqdm import tqdm




def isHate(dico):
	"""
	Just a little function for extract label and score for XTC prediction
	"""

	proba = dico['score']

	if dico['label'] == 'LABEL_0' : 
		return 'non-hateful', 1-proba # we want the proba of having 'hateful'
	else :
		return 'hateful', proba



def run(folder, case, langage):
	"""
	run all cases in the csv `{folder}/{case}/{langage}/cases_final.csv`, with XTC model
	"""

	c.fy(f"Run {case} * {langage}")

	cases = pd.read_csv(f"{folder}/{case}/{langage}/cases_final.csv", index_col=0)
	pipe = pipeline("text-classification", model="Rewire/XTC") #, device=0)

	c.fly(f"Device used by pipeline : {pipe.model.device}")

	nbTest = len(cases['test_case'])
	predictions = list()
	probability = list()

	progress_bar = tqdm(total=nbTest, desc="Progression")

	for i, tc in enumerate(list(cases['test_case'])):
		predi = pipe(tc)
		isH, proba = isHate(predi[0])
		predictions.append(isH)
		probability.append(proba)

		progress_bar.update(1)

	df = cases.copy()
	df['predictions'] = predictions
	df['probability'] = probability

	df.to_csv(f"{folder}/{case}/{langage}/predictions.csv")
	progress_bar.close()



def all_calcul_XTC(folder, force=False):

	c.fm(f"\n======== ALL calcul ========")
	if force : c.fm(f"-> with force")

	for case in os.listdir(folder):

		for langage in os.listdir(f"{folder}/{case}"):

			# extract if cases_final is not exist (or if force)
			if "predictions.csv" not in os.listdir(f"{folder}/{case}/{langage}") or force:

				run(folder=folder, case=case, langage=langage)