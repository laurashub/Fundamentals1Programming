import pandas as pd
import numpy as np
import sys

#Reads in both the expression file and the clusters file we were just playing with
def read_csv(filename, index):
	data = pd.read_csv(filename, index_col=index) 
	return data

"""
For the default value of k (noted by the True in the first column of the clusters file) 
"""
def find_k(df):
	k_row = df[df['sel.K']]
	return k_row.index.values[0], k_row.at[k_row.index.values[0], 'K']

"""
calculate the average expression for each gene within each cluster. 
"""
def cluster_cells(k_index, k, df):
	clusters = {}
	for i in range(1,k+1):
		clusters[i] = []
	for cell in df.columns:
		if "ERR" in cell:
			clusters[df.at[k_index, cell]].append(cell)
	return clusters
	

def calc_expressions(k, clusters, exmat_df):
	#create blank dataframe
	result_df = pd.DataFrame(columns=range(1, k+1), index=exmat_df.index)
	for i in range(1, k+1):
		result_df[i] = exmat_df.loc[:,clusters[i]].mean(axis=1)
	return result_df

#main
exmat = "E-MTAB-7365.csv" #Single-cell RNA seq expression matrix
clusters = "E-MTAB-7365.clusters.csv"#cell cluster assignments for various values of k

exmat_df = read_csv(exmat, 0)
clusters_df = read_csv(clusters, False)

k_index, k = find_k(clusters_df)
clusters = cluster_cells(k_index, k, clusters_df)

results_df = calc_expressions(k, clusters, exmat_df)
print(results_df.to_string())


