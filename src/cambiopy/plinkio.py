import numpy as np
import pandas as pd


#fname=map_data_file
def read_map_file(fname):
    cols = ["chr", "marker", "dist", "pos"]
    data = pd.read_csv(fname, names = cols, sep ='\t')
    return data

#fname = ped_data_file
#snps = marker_names
def read_ped_file(fname, snps):
    cols = ["Family_ID", "Individual_ID", "Paternal_ID", "Maternal_ID", "Sex_M1_F2", "Phenotype"]
    cols.extend(snps)
    data = pd.read_csv(fname, names = cols, sep ='\t')
    return data

if __name__ == '__main__':

    dpath = '/mnt/c/Users/camnu/bin/salmon-euro-introgression/data/May2022_SNPchip_220K/SNPchip_100MS_SNPpanel_King7_Compare/SNPchip_220K/'

    meta_q_data_file = dpath+'panel_data_admix_vals.tsv'
    map_data_file = dpath+'panel_snp_513_set.map'
    ped_data_file = dpath+'panel_snp_513_set.ped'

    # read in the metadata
    fish_data = pd.read_csv(meta_q_data_file , sep ='\t')
    fish_data.head()
    fish_data.shape

    #read in the marker data
    map_data = read_map_file(map_data_file)
    marker_names = list(map_data.marker.values)

    #read in the SNP data
    snp_data = read_ped_file(ped_data_file, marker_names)

    merged_df = pd.merge( fish_data, snp_data, how = 'inner', left_on = "fish_id", right_on = "Individual_ID")

    print("ive got an r function for encoding this, so pivoting to that.")


    