import os
import types
import pytest

from cambiopy.seqio import file_type
from cambiopy.seqio import read_fasta, read_fastq
from cambiopy.seqio import iter_read_fasta, iter_read_fastq
from cambiopy.seqio import write_fasta, write_fastq

from cambiopy import example_fasta, example_fastq
from cambiopy import ex_fasta_file, ex_fastq_file


def test_file_type():
	"""Test that the file type is properly identified."""
	assert file_type("file_1.fa") == "fasta"
	assert file_type("file_1.fasta") == "fasta"
	assert file_type("in.file_1.fa") == "fasta"
	assert file_type("file_2.fq") == "fastq"
	assert file_type("file_2.fastq") == "fastq"
	assert file_type("in.file_2.fq") == "fastq"

	with pytest.raises(ValueError):
		file_type("infile_2.txt")

	with pytest.raises(ValueError):
		file_type("in.file_2.csv")


def test_fasta_reader():
	""" Test the fasta reader functions."""
	fasta_read = read_fasta(ex_fasta_file)
	
	assert len(fasta_read) == 100
	
	assert fasta_read[0]['name'] == "seq1_plantae"
	assert fasta_read[1]['name'] ==	"seq2_bacteria"
	assert fasta_read[2]['name'] == "seq3_protista"

	assert fasta_read[0]['sequence'][:25] == "TTCTAGGAGCATGTATATCTATGCT"
	assert fasta_read[1]['sequence'][:25] == "ACGGGCTTATCATGGTATTTGGTGC"
	assert fasta_read[2]['sequence'][:25] == "AGTATTAATTCGTATGGAATTAGCA"


def test_fastq_reader():
	""" Test the fastq reader functions."""
	fastq_read = read_fastq(ex_fastq_file)

	assert len(fastq_read) == 100

	for i in range(len(fastq_read)):
		assert list(fastq_read[i].keys()) == ['name', 'sequence', 'strand', 'quality']

	assert fastq_read[0]['name'] == "seq1_plantae"
	assert fastq_read[1]['name'] ==	"seq2_bacteria"
	assert fastq_read[2]['name'] == "seq3_protista"

	assert fastq_read[0]['sequence'][:25] == "ttctaggagcatgtatatctatgct"
	assert fastq_read[1]['sequence'][:25] == "acgggcttatcatggtatttggtgc"
	assert fastq_read[2]['sequence'][:25] == "agtattaattcgtatggaattagca"


def test_iter_fasta_reader():

	# read in the data
	data = iter_read_fasta(ex_fasta_file, batch = 10)
	
	assert type(data) == types.GeneratorType

	for d in data:
		assert len(d) == 10
		assert list(d[0].keys()) == ['name', 'sequence']


def test_iter_fastq_reader():

	data = iter_read_fastq(ex_fastq_file, batch = 10)

	assert type(data) == types.GeneratorType

	for d in data:
		assert len(d) == 10
		assert list(d[0].keys()) == ['name', 'sequence', 'strand', 'quality']


def test_fasta_writer():

	orignal_fasta_read = read_fasta(ex_fasta_file)

	with pytest.raises(TypeError):
		write_fasta(orignal_fasta_read) #missing an argument

	with pytest.raises(ValueError):
		write_fasta(orignal_fasta_read,"temp_test/outfile_1.txt")
	
	with pytest.raises(ValueError):
		write_fasta(orignal_fasta_read,"temp_test/outfile_1.fq")

	os.mkdir('temp_test/')

	write_fasta(orignal_fasta_read,'temp_test/test_example_out.fa')

	re_read_fa1 = read_fasta('temp_test/test_example_out.fa')
	
	assert list(re_read_fa1[0].keys()) == ['name', 'sequence']
	assert re_read_fa1[0]['name'] == 'seq1_plantae'
	assert re_read_fa1 == orignal_fasta_read

	os.remove('temp_test/test_example_out.fa')
	os.rmdir("temp_test/")

def test_fastq_writer():

	orignal_fastq_read = read_fastq(ex_fastq_file)

	with pytest.raises(TypeError):
		write_fastq(orignal_fastq_read) #missing an argument

	with pytest.raises(ValueError):
		write_fastq(orignal_fastq_read,"temp_test/outfile_1.txt")

	with pytest.raises(ValueError):
		write_fastq(orignal_fastq_read,"temp_test/outfile_1.fa")

	os.mkdir('temp_test/')

	write_fastq(orignal_fastq_read,'temp_test/test_example_out.fq')

	re_read_fq1 = read_fastq('temp_test/test_example_out.fq')
	orignal_fastq_read = read_fastq(ex_fastq_file)

	assert list(re_read_fq1[0].keys()) == ['name', 'sequence', 'strand', 'quality']
	assert re_read_fq1[0]['name'] == 'seq1_plantae'
	assert re_read_fq1 == orignal_fastq_read

	os.remove('temp_test/test_example_out.fq')
	os.rmdir("temp_test/")
