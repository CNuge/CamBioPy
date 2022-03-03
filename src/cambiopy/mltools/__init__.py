"""
==========
Data and models
==========
ex_fasta_file : str, a path to a fastq file with 100 example COI-5P DNA barcode sequences

ex_fastq_file : str, a path to a fasta file with 100 example COI-5P DNA barcode sequences

example_fasta : list, a list of DNA sequences records. Each record contains data 
	derieved from a fasta file in dictionary format.

example_fastq : list, a list of DNA sequences records. Each record contains data 
	derieved from a fastq file in dictionary format.

"""


import os
import sys
import cambiopy.seqio as seqio

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "CamBioPy"
    __version__ = version(dist_name)
except PackageNotFoundError:
    __version__ = "unknown"  # pragma: no cover
finally:
    del version, PackageNotFoundError


location = os.path.dirname(os.path.realpath(__file__))

ex_fasta_file = os.path.join(location, 'data', 'example_data.fasta')
ex_fastq_file = os.path.join(location, 'data', 'example_data.fastq')

example_fasta = seqio.read_fasta(ex_fasta_file)
example_fastq = seqio.read_fastq(ex_fastq_file)
