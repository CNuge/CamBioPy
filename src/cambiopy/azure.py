#!/bin/env/python3
import sys
import os
import argparse

#location = '.'
#suffix = '.py'
def get_filelist(location, suffix = None, recursive = False):
	""" Get a list of files in a directory and optionally its subdirs,
		 with optional suffix matching requirement."""
	if recursive == False:
		if suffix is None: 
			filelist = [location+x for x in os.listdir(location)]
		else:
			filelist = [location+x for x in os.listdir(location) if x[-len(suffix):] == suffix]

	elif recursive == True:
		filelist = []
		for path, subdirs, files in os.walk(location):
			for x in files:
				if suffix is None or x[-len(suffix):] == suffix:
					rpath = os.path.join(path, x)
					filelist.append(rpath)

	return filelist


def build_to_azure_calls(files, local_location, azure_location, 
							keep_structure = True, 
							relative_paths = False, 
							trim_local_paths = None):
	""" Take a list of local relative filepaths and build azure transfer calls

		If keep_structure == true, the subfolders will be added to the azure calls.
		Note for the retention of structure, only subfolders of the current working
		directory will be valid (no higher levels in file heirarchy permitted)

		"""
	outlist = []
	for f in files:
		if keep_structure == False:
			outstr = f'azcopy copy "{f}" "{azure_location}"\n'
		else:
			if relative_paths == True:
				if f[:2] != './':
					raise ValueError("The keep_structure argument requires relative imports (leading dotslash ('./')")
				parts = f[2:].split("/")
			else:
				parts = f.split("/")

			add_path = "/".join(parts[:-1])
			add_path+="/"
			#second bit of logic here is to avoid the double end slash when not
			#including any subfolders
			if trim_local_paths is None and add_path != "/":
				outstr = f'azcopy copy "{f}" "{azure_location}{add_path}"\n'
			else:
				az_path = add_path.replace(local_location, '')
				outstr = f'azcopy copy "{f}" "{azure_location}{az_path}"\n'
		outlist.append(outstr)

	return outlist


def build_from_azure_calls(files, azure_location, local_location = "."):
	""" Take a list of files and their location on azure and build transfer calls
		to move them to a specified local location."""
	outlist = []

	for f in files:
		outstr = f'azcopy copy "{azure_location}{f}" "{local_location}"\n'
		outlist.append(outstr)

	return outlist


def read_filelist(file):
	""" Read in a list of files for transfer FROM azure to local."""
	dat = []
	with open(file, "r") as f:
		for line in f:
			line = line.rstrip()
			dat.append(line)
	return dat


def write_calls_file(calls, outfile):
	""" Take the produced azcopy file-by-file calls and write the output script """
	f=open(outfile, 'w')
	for line in calls:
		f.write(line)
	f.close()
