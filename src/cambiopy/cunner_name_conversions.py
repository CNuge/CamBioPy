
"""
note the order of the numbers was scrambled, as I think the final file had the chrs
listed by size, but the numbering was based off the previous version of the genome
so things got reshuffled after the last genome update
"""
vgp_nov10 = ["SUPER_2", "SUPER_4", "SUPER_5", "SUPER_6", "SUPER_3",
				"SUPER_7", "SUPER_9", "SUPER_12", "SUPER_13", "SUPER_1",
				"SUPER_14", "SUPER_16", "SUPER_15", "SUPER_17", "SUPER_10",
				"SUPER_18", "SUPER_19", "SUPER_11", "SUPER_20", "SUPER_21",
				"SUPER_8", "SUPER_22", "SUPER_23", "SUPER_24",]

"""
I've not confirmed, but think this should be the equivalent order to the vgp_nov10
naming, this can be checked by comparing the chr sizes after the genome update is
fully posted on ncbi
"""
ncbi = ["CM036534.1", "CM036535.1", "CM036536.1", "CM036537.1",
		"CM036538.1", "CM036539.1", "CM036540.1", "CM036541.1",
		"CM036542.1", "CM036543.1", "CM036544.1", "CM036545.1",
		"CM036546.1", "CM036547.1", "CM036548.1", "CM036549.1",
		"CM036550.1", "CM036551.1", "CM036552.1", "CM036553.1",
		"CM036554.1", "CM036555.1", "CM036556.1", "CM036557.1",]


def vgp2ncbi_dict(vgp_nov10 = vgp_nov10, ncbi = ncbi):
	return {k: v for k, v in zip (vgp_nov10, ncbi)}

def ncbi2vgp_dict(vgp_nov10 = vgp_nov10, ncbi = ncbi):
	return {k: v for k, v in zip(ncbi, vgp_nov10)}

def vgp2numeric_dict(vgp_nov10 = vgp_nov10):
	return {x: i for i, x in enumerate(vgp_nov10)}

def numeric2vgp_dict(vgp_nov10 = vgp_nov10):
	return {i: x for i, x in enumerate(vgp_nov10)}

def ncbi2numeric_dict(ncbi = ncbi):
	return {x: i for i, x in enumerate(ncbi)}

def numeric2ncbi_dict(ncbi = ncbi):
	return {i: x for i, x in enumerate(ncbi)}



if __name__ == '__main__':
	
	"""
	#use in other scripts
	from name_conversions import vgp2ncbi_dict

	#or if you've got the module installed
	from cunner_genome.name_conversions import vgp2ncbi_dict
	# and just import the one you want!

	"""

	vgp2ncbi_dict()
	
	ncbi2vgp_dict()
	
	vgp2numeric_dict()
	
	numeric2vgp_dict()
	
	ncbi2numeric_dict()
	
	numeric2ncbi_dict()