import numpy as np
import pandas as pd

from Bio import SeqIO


def calc_bp_composition(seq):
    """ Take a sequence of DNA and count the nucleotide composition."""
	counts = {"A" : 0,
				"T" : 0,
				"G" : 0,
				"C" : 0,
				"N" : 0,
				"other" : 0}
	for i in seq:
		if i in counts.keys():
			counts[i] += 1
		else:
			counts["other"] += 1
	return counts


def gc_content(counts):
    """ Determine GC content from nucleotide count dict.

    	Count is given using on;y the non missing bp (i.e. g+c / (c+g+a+t))."""
    gc_count = counts['G'] + counts['C']

    total = counts['A'] + counts['T'] + counts['G'] + counts['C']

    return gc_count / total


def missing_info(counts):
    """ How many non standard nucleotides are in the sequence?"""
    bad_count = counts['N'] + counts['other']

    total = counts['A'] + counts['T'] + counts['G'] + counts['C'] + counts['N'] + counts['other']

    return bad_count / total


def sequence_gc_content(sequence):
	""" Calculate the GC content of the sequence.

		N.B. unknown (N) nucleotides are not included in the calculation."""

	bp_counts = calc_bp_composition(sequence)

	return gc_content(bp_counts)