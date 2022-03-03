import random
import numpy as np
import pandas as pd


def get_truth_sets(max_flip = 100, one_change = True, 
						transition = None, samples = None,
						binary_states = ["H", "T"]):
	""" generate example strings with either:
	 		- all of the combinations single transitions
	 		- random changes
	 				in this case a transition probability and a number of samples to
	 				generate must be specified """
	s1 = binary_states[0]
	s2 = binary_states[1]

	if one_change == True:
		combos = [s1 * x + s2 * (max_flip - x) for x in range(max_flip+1)]

	elif one_change == False:

		combos = []

		for i in range(samples):

			current = random.sample([0,1], 1)[0]
			s = binary_states[current]

			for i in range(1, max_flip):
				val = random.uniform(0, 1)
				if val < transition:
					if current == 0:
						current = 1
					elif current== 1:
						current = 0
				s+=binary_states[current]

			combos.append(s)
	return combos


def gen_obv(true_val, h_see_t = 0.3820, t_see_h = 0.4625):
	"""
	given a true value (hidden state), generate an observed state
	using the false prediction probabilities."""

	assert true_val == "H" or true_val == "T"

	val = np.random.random_sample()

	if true_val == "H":
		if val < h_see_t:
			return "T"
		else:
			return "H"

	elif true_val == "T":
		if val < t_see_h:
			return "H"
		else:
			return "T"


def get_truth_obvs_pair(true_str):
	"""Take in a true string, generate a true str, obvs str pair in dict format."""

	new_str = ''

	for c in true_str:
		obvs_c = gen_obv(c)

		new_str += obvs_c

	out_dict = {'true': true_str, 
				'obvs' : new_str}

	return out_dict


if __name__ == '__main__':
	
	simulation_pairs = []

	truth_sets = get_truth_sets()
	#or
	rand_truth_sets = get_truth_sets(one_change = False, 
						transition = 0.1, samples = 100)


	for x in range(1000):

		for t in truth_sets:
			hmm_dict = get_truth_obvs_pair(t)

			simulation_pairs.append(hmm_dict)


	out_df = pd.DataFrame(simulation_pairs)
	out_df.head()

	out_df.to_csv('simulated_data.tsv', sep = '\t', index = False)

	# these will be the ground truth labels.
	# for each ground truth, create a set simulated observations
	# insert errors into the observed states based on the probabilities learned
	# in get_error_data.r

	# will end up with tuples like this
	# actual: PPPPPPOOOOOOO     obvs: POPPPPOOOPOOO

	#