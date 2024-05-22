import os
import pandas as pd
import csv
import coloralf as c
import numpy as np


def extractIDEN(folder, case, langage):
	"""
	Extraction of differente targets for `case` and `langage`

	Param :
		- folder [str]  : folder name where there are cases folders
		- case [str]    : Maybe be confusing but it's the "point of interest". 
			-> For example, "hatecheck_base" for all targets give in Hate Check
			-> "nationality" for all targets I write
		- langage [str] : Choose the langage for targets
	"""

	# recup of targets csv, check files to see the format
	iden = pd.read_csv(f"{folder}/{case}/{langage}/IDENT.csv")

	idents = dict()
	cols = list(iden.columns)[1:]

	for i in range(iden.shape[0]):

		# for each target, I extract words associate with the targets (male singular, male plurial, female singular with ...)

		target = iden['TARGET'].iloc[i]
		elements = iden[cols].iloc[i].values

		for element, col in zip(elements, cols):

			if len(element) > 1:

				if col not in idents.keys():
					idents[col] = list()

				idents[col].append([target, element])

	return idents


def extract(folder, case, langage):

	'''
	Make all cases, combined templates & IDENT present in folder/case/langage


	Correction templates french : 
		templ_id 527 -> add gender_female because doesn't exist
		templ_id ??? -> correction [females_IDENT_P] -> [female_IDENT_P]
	'''

	c.fy(f"Creation for {case} * {langage}")

	# read templates and extract targets (IDENT)
	temp = pd.read_csv(f"{folder}/{case}/{langage}/templates.csv")
	idents = extractIDEN(folder, case, langage)

	df = pd.DataFrame(columns=['case_id', 'functionality', 'test_case', 'label_gold', 'target_ident'])

	# colomns needed
	columns_study = ['functionality', 'label_gold', 'trans_manual'] 

	# add gender colomns for langage which have gender case
	if 'gender_male' in temp.columns and 'gender_female' in temp.columns:
		columns_study += ['gender_male', 'gender_female']
		c.flk(f"INFO : gender cases ok !")
		gender_case = True
	else:
		c.flk(f"INFO : no gender case for this langage !")
		gender_case = False
	
	# create dict just for containt the number of each mask detected
	nb = dict()

	# we iterate on all templates
	for i in range(temp.shape[0]):

		# we recup wanted columns
		if gender_case:
			func, label, neutral, male, female = temp[columns_study].iloc[i].values
		else:
			func, label, neutral = temp[columns_study].iloc[i].values
			male, female = None, None

		# Each template can have on or two sentence, depend if we have neutral sentence or male/female sentense
		tempHere = list()

		# if the template sentence not neutral, there is a `-` in the csv, it's for that that I test if len(neutral) > 4 
		if type(neutral) is str and len(neutral) > 4:
			tempHere.append(neutral)
		elif type(male) is str and type(female) is str and (len(male) > 4 or len(female) > 4):
			if len(male) > 4   : tempHere.append(male)
			if len(female) > 4 : tempHere.append(female)
		else:
			# In case if I detect nothing, or male or female missing
			c.fr(f"WARNING [extract] : Ni neutral ni male/female it's very weird...")
			c.fr(f"Index {i} : ")
			c.fr(f"- neutral    : {c.m}{neutral}{c.d}")
			c.fr(f"- male       : {c.m}{male}{c.d}")
			c.fr(f"- female     : {c.m}{female}{c.d}")

		# we iterate on each sentences
		for tempI in tempHere:


			# There is a maks ? 
			if '[' in tempI and ']' in tempI:
				ind0 = tempI.index('[')
				ind1 = tempI.index(']')
				mask = tempI[ind0:ind1+1]
			else:
				mask = 'nan'


			# We replace mask by each target, and we push the result in the DataFrame df
			if 'IDENT' in mask and mask in idents.keys():

				for target, placeholder in idents[mask]:

					if target not in nb.keys() : nb[target] = 0
					nb[target] += 1

					df = df._append({'case_id':f"{langage}-{df.shape[0]}",  'functionality':func,  'test_case':tempI.replace(mask, placeholder), 'label_gold':label, 'target_ident':target}, ignore_index=True)

			elif mask == 'nan':

				if 'neutre' not in nb.keys() : nb['neutre'] = 0
				nb['neutre'] += 1

				df = df._append({'case_id':f"{langage}-{df.shape[0]}",  'functionality':func,  'test_case':tempI, 'label_gold':label, 'target_ident':'neutre'}, ignore_index=True)

			elif 'SLR' or 'IDENT' in mask:

				# we don't need of this
				pass

			else:
				# If we are a weird mask
				c.fr(f"WARNING [extract] : Unknow mask ??? -> {mask}")
				c.fr(f"Index {i} : ")
				c.fr(f"- neutral    : {c.m}{neutral}{c.d}")
				c.fr(f"- male       : {c.m}{male}{c.d}")
				c.fr(f"- female     : {c.m}{female}{c.d}")

	c.flb(f"Mask applied : ")
	[print(f" - {key} = {val}") for key, val in nb.items()]

	c.flb(f"Total cases mades : ")
	print(f" -> {df.shape[0]}")

	# save ...
	df.to_csv(f"{folder}/{case}/{langage}/cases_final.csv")




def all_creation_cases(folder, force=False):

	c.fm(f"\n======== ALL creation cases ========")
	if force : c.fm(f"-> with force")

	for case in os.listdir(folder):

		for langage in os.listdir(f"{folder}/{case}"):

			# extract if cases_final is not exist (or if force)
			if "cases_final.csv" not in os.listdir(f"{folder}/{case}/{langage}") or force:

				extract(folder=folder, case=case, langage=langage)