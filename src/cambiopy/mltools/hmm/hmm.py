
from pomegranate import *


def hmm(
		heads_emissions = {"H": 0.7, "T": 0.3},
		tails_emissions = {"H": 0.334, "T": 0.666}):
	"""

	Given emission probabilities, initalize a hidden markov model.

	The initial model can be furtuer trained using the viterbi algorithm
	and simulated label data.

	you'll have to change the transition probabilities to informed priors 
	"""
	model = HiddenMarkovModel()

	#these were determined by looking at the real data values
	dist_heads_emission = DiscreteDistribution(heads_emissions)
	dist_tails_emission = DiscreteDistribution(tails_emissions)

	heads_state = State(dist_heads_emission, name = "heads")
	tails_state = State(dist_tails_emission, name = "tails")


	model.add_states([heads_state, tails_state])

	model.add_transition(model.start, heads_state, 0.5)
	model.add_transition(model.start, tails_state, 0.5)

	# note the heads -> and tails -> add up to less than 1
	# rest of prob goes to exit probability
	model.add_transition(heads_state, heads_state, 0.75)
	model.add_transition(heads_state, tails_state, 0.15)
	model.add_transition(tails_state, heads_state, 0.2) 
	model.add_transition(tails_state, tails_state, 0.8)

	model.add_transition(tails_state, model.end, 0.1)
	model.add_transition(heads_state, model.end, 0.1)

	model.bake()

	return model


def get_path(sequence, model):
	""" for a given sequence of observations and HMM model, 
		generate the predicted series of hidden states using 
		the viterbi algorithm."""
	prob, states = model.viterbi(sequence)

	path = [state[1].name for state in states ]
	return path

if __name__ == '__main__':
	
	hmmr = hmm()


	# get these from your simulated data
	#hmmr.fit(sequences = obvs_seqs, labels = true_labels, algorithm = 'labeled')


	s = list('HHHHHHHHHTTHHHHHHHH')
	get_path(s, hmmr)

	s = list('TTTTTHHHHHHHHTTTTT')
	get_path(s, hmmr)

	combos = ['H' * x + 'T' * (91 - x) for x in range(91)]

	combos[55]

	get_path(combos[55], hmmr)

	get_path(combos[77], hmmr)
