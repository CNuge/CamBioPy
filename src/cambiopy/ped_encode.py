import numpy as np
import pandas as pd

def readPedMap_tsv_fmt(ped_file, map_file = "", headers = False):
    
    col_names = ["chromosome", "snp" , "genetic_distance", "physical_distance"]

    if headers == True:
        map_data = pd.read_csv(map_file, skiprows = 0, names = col_names, sep = '\t')
        
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        header_data.extend(snp_columns)

        snp_data = pd.read_csv(ped_file, skiprows = 0, names = header_data, sep = '\t')
        return snp_data, snp_columns
        
    else:
        
        map_data = pd.read_csv(map_file, names = col_names, sep = '\t')
        
        header_data = ['#family', 'individual', 'sire', 'dam', 'sex', 'pheno']
        snp_columns = list(map_data['snp'].values)
        header_data.extend(snp_columns)
        
        snp_data = pd.read_csv(ped_file, names = header_data, sep = '\t')
        return snp_data, snp_columns



def get_unique_alleles(gt_count_dict):
    """Determine the major and minor alleles for the given marker."""
    unique_alleles = {}
    for x in gt_count_dict.keys():
        for a in x.split(" "):
            if a in unique_alleles.keys():
                unique_alleles[a] = unique_alleles[a] + gt_count_dict[x]
            else:
                unique_alleles[a] = gt_count_dict[x]
    if len(unique_alleles) > 2:
        raise ValueError("SNP is not biallelic")
    if len(unique_alleles) == 1:
        raise ValueError("SNP is homozygous")
    k1, k2 = unique_alleles.keys()
    if unique_alleles[k1] >= unique_alleles[k2]:
        return k1, k2
    else:
        return k2, k1


def calc_mode(snp_arr):
    """get the most common value in the array of SNP values. For imputing missing info"""
    vals, counts = np.unique(snp_arr, return_counts=True)
    index = np.argmax(counts)
    return vals[index]


#  snp_arr = snp_data[x].values
#' Homozygous for major allele encoded as 0, heterozygoous = 1, Homozygous minor allele = 2
#' method - make it so you can do one hot, dosage, or presence/absence. currently just dosage
#' missing_data - can put in the mode or NA
def dosage_encode_snps(snp_arr, missing_val = "0 0", replace_missing_method = "mode"):
  #determine the major and minor alleles

    if replace_missing_method == "mode" :

        mode_gt = calc_mode(snp_arr)
        if mode_gt == missing_val:
            raise ValueError("most common allele is a missing genotype!")

        snp_arr[snp_arr == missing_val] = mode_gt
        
    vals, counts = np.unique(snp_arr, return_counts=True)
    gt_count_dict = {k : v for k, v in zip(vals, counts)}

    p, q = get_unique_alleles(gt_count_dict)
 
    encodings = {f"{p} {p}" : 0,
                    f"{p} {q}" : 1,
                    f"{q} {p}" : 1,
                    f"{q} {q}" : 2}

    encoded_data = [encodings[x] for x in snp_arr] 

    return encoded_data




#'
#' method - make it so you can do one hot, dosage, or presence/absence. currently just dosage
def encode_ped(snp_data, snp_columns, method = "dosage" ):
    #x = snp_columns[2]
    for x in snp_columns:
        #print(x)
        snp_data[x] = dosage_encode_snps(snp_data[x].values)
    return snp_data









if __name__ == '__main__':

    dpath = "/mnt/c/Users/camnu/bin/salmon-euro-introgression/data/May2022_SNPchip_220K/SNPchip_100MS_SNPpanel_King7_Compare/SNPchip_220K/"

    ped_file = dpath+'panel_snp_513_set.ped'
    map_file = dpath+'panel_snp_513_set.map'

    meta_data = dpath+'panel_data_admix_vals.tsv'
    meta_df = pd.read_csv(meta_data, sep = '\t')

    snp_data, snp_columns = readPedMap_tsv_fmt(ped_file, map_file)

    assert len(snp_columns) == 513

    snp_data = encode_ped(snp_data, snp_columns)

    meta_df['individual'] = meta_df['fish_id'].values

    all_shared = pd.merge(meta_df, snp_data, how = 'inner')

    all_shared.to_csv(dpath+"encoded_snp_panel_with_metadata.tsv", sep = '\t', index=False)

