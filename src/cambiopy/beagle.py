import numpy as np
import pandas as pd
from cambiopy.filelists import lines_to_file


def read_beagle(filename, sample_list, header = True):
	"""Take a path to a beagle file and list of samples in the file, 
		read in the file and add the header information.

		returns a df and a dictonary with the names of columns corresponding
		to each sample in the sample_list """

	print("building the header information")
	beagle_header = ["marker", "allele1", "allele2", ]

	col_dict = {} #sample_id : cols

	for ind in sample_list:

		ind_cols = [f'{ind}_probAA', f'{ind}_probAB', f'{ind}_probBB']

		beagle_header.extend(ind_cols)

		col_dict[ind] = ind_cols

	print("loading the beagle file")
	if header == True:
		beagle_df = pd.read_csv(filename, names = beagle_header, sep = '\t', skiprows = 1)
	else:
		beagle_df = pd.read_csv(filename, names = beagle_header, sep = '\t')

	return beagle_df, col_dict


def write_beagle(df, outfile, header = None,):

	if header is None:
		df.to_csv(outfile, header=False, sep = '\t', 
							index=False, float_format='%.6f')
	else:
		assert type(header) == str

		lines_to_file([header], outfile, add_newline=True)
		df.to_csv(outfile, mode='a', header=False, sep ='\t', 
							index = False,  float_format='%.6f')


def build_generic_header(keep_samples):
	out = ["marker", "allele1", "allele2", ] 
	for i, _ in enumerate(keep_samples):
		dat = [f'Ind{i}'] * 3
		out.extend(dat)
	return '\t'.join(out)


if __name__ == '__main__':
	
	#example usage below:

		
	#get the list of samples in the original beagle
	sample_file = "/scratch/nugentc/data/analysis-cunner-snps/data/full_sample_list.txt"
	#sample_file = "../data/full_sample_list.txt"
	sample_list = pd.read_csv(sample_file,  names = ["ID"])

	#for scaling on the server
	raw_beagle = "/scratch/nugentc/data/analysis-cunner-snps/data/raw/merged.beagle"
	#raw_beagle = "../data/downsampled/mini_merged.beagle"
	beagle_df, col_dict = read_beagle(raw_beagle, sample_list.ID.values)

	# remove the two outlier locations
	# note the sample order must be saved along with the output beagle file
	# so that the data can be read into r and properly mapped back to the
	# sample of origins.
	keep_samples = [x for x in sample_list.ID.values 
						if "TUK" not in x and "DIB" not in x]

	keep_cols = ["marker", "allele1", "allele2", ]
	
	out_header = build_generic_header(keep_samples)

 	for s in keep_samples:
 		keep_cols.extend(col_dict[s])

 	# double check there are
 	# three cols per sample, plus three leading columns
 	assert (len(keep_cols) - 3) == (len(keep_samples)*3)

	#beagle_out = "../data/downsampled/subset_merged.beagle"
	beagle_out = "/scratch/nugentc/data/analysis-cunner-snps/data/raw/subset_merged.beagle"
	#sample_file_out = "../data/subset_sample_list.txt"
	sample_file_out = "/scratch/nugentc/data/analysis-cunner-snps/data/subset_sample_list.txt"

	selected_beagle = beagle_df[keep_cols]

	write_beagle(selected_beagle, beagle_out, header = out_header)

	lines_to_file(keep_samples, sample_file_out, add_newline = True)
