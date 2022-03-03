import os
import pickle

import numpy as np
import pandas as pd

import plotly
import plotly.express as px

from sklearn.decomposition import PCA
from sklearn.preprocessing import  StandardScaler

def quick_scatter_plot(df, x, y, color, alpha = 0.5, filename = 'out.html'):
	""" take a dataframe and spcified x, y, and colouration columns and make a scatter plot."""
	fig = px.scatter(df, x = x, y = y, color = color, opacity = alpha)

	plotly.offline.plot(fig, filename = filename) 

	return fig


def scale_predictors(df, predictors, scaler = None):
    """ standard scale the specified columns of the pandas dataframe. """

    if scaler == None:
        scaler = StandardScaler()
        df[predictors] = scaler.fit_transform(df[predictors])
    else:
        df[predictors] = scaler.transform(df[predictors])

    return df, scaler


def run_pca(df, predictors, n_components = 7):
	""" take a dataframe, specified predictors, and number of components and run a PCA. 

		returns tuple of the PCA model and the principal components (in that order)"""
	X_train = df[predictors]

	pca = PCA(n_components = n_components)
	pca_result = pca.fit_transform(X_train.values)

	return pca, pca_result


def plot_pairwise_pca(pca, components, classification, 
						alpha = 0.2, filename = 'out.html'):
	""" Take a principal component model, outputs and classification vector and make 
		pairwise plots. """
	labels = {
		str(i): f"PC {i+1} ({var:.1f}%)"
		for i, var in enumerate(pca.explained_variance_ratio_ * 100)
	}

	fig = px.scatter_matrix(
		components,
		labels=labels,
		dimensions=range(components.shape[1]),
		color=classification,
		opacity = alpha
	)

	plotly.offline.plot(fig, filename = filename) 

	return fig


if __name__ == '__main__':
	
	#read in the data frame - this is a path to a tsv 
	data = pd.read_csv('train.tsv', sep = '\t')

	#if very large, take a smaller sample, for faster iteration on the plotting and smaller html outputs
	train = data.sample(int(len(data)*0.01))
	train.shape
	#otherwise make train a pointer to the raw df
	# train = data

	#select predictors columns to scale, only the predictor variables 
	all_predictors = ['marker1', 'marker2']

	#standard scale all the predictors
	train, _ = scale_predictors(train, all_predictors)
	#or if you want to keep the scaler:
	#train, scaler = scale_predictors(train, all_predictors)

	#select the features to consider in the PCA, if different from the complete set
	pca_predictors = ['marker1', 'marker2']
	#else, a pointer again
	pca_predictors = all_predictors

	#run the pca using the relevant cols from the relevant df
	pca_model, pca_result = run_pca(train, pca_predictors, n_components = 4)

	#could save the scaler model or pca for resue here
	#pickle.dump(pca_model, open('pca.pkl', 'wb'))
	#pickle.dump(scaler, open('scaler_pca.pkl', 'wb'))

	#create an interactive plot of all the pairwise PC combinations
	#model passed in solely for axis labels
	plot_pairwise_pca(pca_model, pca_result, classification = train['class'].values, 
								filename = 'PCA_by_a_category.html')

	quick_scatter_plot(train, 
                        x = "pca-one", 
						y = "pca-two", 
						color = "lact",
						alpha = 0.2,
						filename = "pc1_pc22_scatter_plot.html")