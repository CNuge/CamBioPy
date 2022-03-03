from ast import Raise
from allel import read_vcf

""" This is a wrapper for using some of the functions in the scikit-allel api

    Ways to grab key things out of a vcf, or hopefully write them in.

    Currently a work in process

    code source: https://scikit-allel.readthedocs.io/en/stable/
"""

def check_vcf(x):
    try:
        assert x.endswith('.vcf') or x.endswith('.vcf.gz')
    except:
        Raise ValueError("vcf processing fuunction - input must have the extension .vcf or .vcf.gz")


def read_genotypes(input_vcf):
    """ Read in a vcf file (can be gzipped) using the scikit-allel function. """



    vcf=allel.read_vcf(infile,log=sys.stderr)
    gen=allel.GenotypeArray(vcf['calldata/GT'])
    samples=vcf['samples']



if __name__ == "__main__":