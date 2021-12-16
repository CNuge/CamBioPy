#!/bin/env/python3
import sys
import os
import argparse

from cambiopy.azure import build_to_azure_calls, build_from_azure_calls
from cambiopy.azure import get_filelist, read_filelist, write_calls_file

#	direction = 'to'
#	suffix = '.fastq.gz'
#	recursive = True
#	local_location = '/scratch/nugentc/data/cunner_reseq/'
#	azure_location = 'https://marinegenomestorage.blob.core.windows.net/cunner/OCTreseq/'
#	outfile = '11-22_azure_new_fq_backup_calls.sh'

def az_parser(args):
	parser  = argparse.ArgumentParser(prog = "azcopy specific file-by-file call builder",
		description = """
		Create a shell script containing file-by-file azcopy command to allow for
		backup of only specific information based on location and file suffixes.
		""")
	parser.add_argument("-l", "--local_location", type=str, default="./" ,
		help = "The local directory to get files from for use in the data transfers to azure.\n"+\
		"or the location to place files in transfers from azure\n")
	parser.add_argument("-a", "--azure_location", type=str,
		help = "The azure url and filepath for use in the transfers.\n")	
	parser.add_argument("-d", "--direction", type=str, default="to" ,
		help = "Specify the direction of the azcopy transfer.\n"+\
		"Input can be either 'to' (to azure from local) or 'from' (from azure to local)\n"+\
		"Default is 'to'.")
	parser.add_argument("-s", "--suffix", type=str, default=None ,
		help = "Suffix to limit the azcopy command generation to a specific type of file.")
	parser.add_argument("-r", "--recursive", dest="recursive", action='store_true',
		help = "For transfers to Azure only.\n"+\
			"Pass this flag if the contents of all subfolders of the local_location\n"+\
			"should be considered for copying. Default is False (just the given directory).")
	parser.add_argument("-o", "--outfile", type=str, default="azcalls.sh" ,
		help = "The name of the file to be created that will contain the list\n"+\
			"of generated azcopy commands. Default is a file named 'azcalls.sh'\n")
	parser.add_argument("-f", "--filelist", type=str, default=None ,
		help = "For direction='from' transfers this file is required"+\
			"The name of a file that contains the list of remote files to copy.\n"+\
			"Each filename should be specified on a separate line.\n")
	parser.add_argument("-k", "--keep_structure", dest="keep_structure", action='store_true',
		help = "For 'to' file transfers using the recursive argument"+\
			"Pass this flag if you with for the nested folder structure should be maintained (True)\n"+\
			"By default data are flattened and all files placed in the same azure folder (False).\n"+\
			"Default is True.\n")
	parser.set_defaults(recursive=False,
						keep_structure=False)
	return parser.parse_args(args)


def main():
	parsed_args = az_parser(sys.argv[1:])
	direction = parsed_args.direction
	suffix = parsed_args.suffix
	recursive = parsed_args.recursive
	local_location = parsed_args.local_location
	azure_location = parsed_args.azure_location
	outfile = parsed_args.outfile
	filelist = parsed_args.filelist
	keep_structure = parsed_args.keep_structure
	if direction == 'to':
    	#files is the list of local filenames joined with the local_location path
		files = get_filelist(local_location, suffix = suffix, recursive = recursive)
		az_calls = build_to_azure_calls(files, local_location, azure_location, 
												keep_structure = keep_structure, 
												relative_paths = False, 
												trim_local_paths = local_location)

	elif direction == 'from':
		if filelist == None:
			raise ValueError("For transfers where direction is 'from', a file "+\
				"containing a list of files to copy from azure must be provided")
		files = read_filelist(filelist)
		az_calls = build_from_azure_calls(files, azure_location, local_location = local_location)

	else:
		raise ValueError("must specify call direction as 'to' or 'from'")

	print("writing calls to file")
	write_calls_file(az_calls, outfile)

	return 1

if __name__ == '__main__':
	#build a shell script containing file-by-file azcopy calls for everything in a directory
	#contains the option to limit the calls to a certain file by suffix.	
	main()

	"""


	direction = 'to'

	suffix = '.fastq.gz'

	recursive = True
	
	local_location = '/scratch/nugentc/data/cunner_reseq/'

	azure_location = 'https://marinegenomestorage.blob.core.windows.net/cunner/OCTreseq/'

	outfile = '11-22_azure_new_fq_backup_calls.sh'

	if direction == 'to':
		files = get_filelist(local_location, suffix = suffix, recursive = recursive)
		az_calls = build_to_azure_calls(files, azure_location, 
												keep_structure = True, 
												relative_paths = False, 
												trim_local_paths = local_location)

	elif direction == 'from':
		filelist = read_filelist()
		az_calls = build_from_azure_calls(filelist, azure_location, local_location = local_location)

	else:
		raise ValueError("must specify call direction as 'to' or 'from'")

	print("writing calls to file")
	write_calls_file(az_calls, outfile)
	"""

