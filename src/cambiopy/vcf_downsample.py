import random
import numpy as np

from cambiopy.filelists import lines_to_file


def vcf_subsample(infile, outfile, sample_freq=0.01):
	""" read a whole vcf into memory, keep all lines with header information
		and then sample a defined percentage of the remainder. 

		Note: vcf must fit in memory for this method to work, otherwise a solution
		using batch loading and sampling will be required."""

	header_max = -1 #keep a pointer to the last header line, assumes they're all sequential
	data = [] #load all the lines into memory

	print("loading data and identifying header")
	with open(infile, 'r') as file:
		for i, line in enumerate(file):
			if line[0] == "#":
				#if new header line found, record the position
				#assumes there won't be random header lines in middle of vcf
				header_max = i
			data.append(line)

	print("writing header to new file")
	lines_to_file(data[:header_max+1], outfile, add_newline=False, mode='w')

	del data[:header_max+1] #delete the header lines prior to sampling

	data = np.array(data) #make the list of lines an array (for ease of slicing)
	print("generating subsample")
	subsample_sz = int(len(data) * sample_freq) #define number of lines to sample

	#get a sorted list of random index positions from the list of data lines
	#note, this is better than sampling the lines themselves as we only
	#keep one copy in memory this way
	keep_indices = sorted(random.sample(range(0, len(data)), subsample_sz))

	print("writing selected subsample to file")
	lines_to_file(data[keep_indices], outfile, add_newline=False, mode='a')

	print("done")


if __name__ == '__main__':


	infile = 'data/examples/example_partial.vcf'
	outfile = 'data/examples/downsampled_example_partial.vcf'
	sample_freq = 0.01

	vcf_subsample(infile, outfile, sample_freq)


	vcf_subsample(infile, 'data/examples/downsampled_example_partial_bigger.vcf', 0.1)



