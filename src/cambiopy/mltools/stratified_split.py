import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedShuffleSplit

def stratified_train_test(input_data, class_col, test_size = 0.2):
	"""
	Take a dataframe and conduct stratified a train/test split based of a 
	user defined categorical column.

	Default is train as 80% of input data.
	Output is two dataframes: train, test
	"""
	print(f'Conducting train/test split, split evenly by: {class_col}')

	strat_index = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=1738)

	for train_index, test_valid_index in strat_index.split(input_data, input_data[class_col]):
		train, test = input_data.loc[train_index], input_data.loc[test_valid_index] 


	return train, test



if __name__ == '__main__':


    data = pd.read_csv('data.tsv', sep = '\t')

    train, test = stratified_train_test(data, 'label_column')


    #if you wish to output them to a single df
    train['dataset'] = 'train'
    test['dataset'] = 'test'

    all_dat = train.append(test)
    all_dat.to_csv('train_test_data.tsv' , sep = '\t', index = False)
