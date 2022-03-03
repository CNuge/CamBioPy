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


def vcf_to_df(input_vcf):
    """ Read in a vcf file (can be gzipped) using the scikit-allel function. """


    vcf=read_vcf(input_vcf)


print("TODO: ")
print("Figure out what of this information I'd like to store into a dataframe and work to build the data structure")
print("keep it flexible, but get from this dict of array's to something more tidy")

vcf.keys()


vcf['samples'].shape
vcf['calldata/GT'].shape #these are arrays of [0,0], [1,0],  [1,1] 

vcf['samples']
vcf['calldata/GT']


vcf['variants/ALT'][0]
vcf['variants/CHROM'][0]
vcf['variants/FILTER_PASS'][0]
vcf['variants/ID'][0]
vcf['variants/POS'][0]
vcf['variants/QUAL'][0]
vcf['variants/REF'][0]



if __name__ == "__main__":


    input_vcf = "data/raw/example_file.vcf"

    