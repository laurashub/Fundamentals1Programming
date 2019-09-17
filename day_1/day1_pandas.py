import pandas as pd
import numpy as np
import sys

#Reads in both the expression file and the clusters file we were just playing with
def read_csv(filename):
	data = pd.read_csv(filename, index_col=False) 
	return data

"""
For the default value of k (noted by the True in the first column of the clusters file) 
"""
def find_k(df, k_col, selK_col):
	for i, x in enumerate(np.nditer(df[k_col].values)):
		if df[selK_col][i]:
			return x
	print("Error: K not found")
	sys.exit(-1)

"""
calculate the average expression for each gene within each cluster. 
"""
def make_clusters(df):
	

"""
To do this with any efficiency, I would recommend starting by creating a dictionary of cell identifiers
to cluster numbers. You will probably also need to create a dictionary of cell identifiers to columns in 
the expression table.
"""


#main
exmat = "E-MTAB-7365.csv" #Single-cell RNA seq expression matrix
clusters = "E-MTAB-7365.clusters.csv"#cell cluster assignments for various values of k

exmat_df = read_csv(exmat)
clusters_df = read_csv(clusters)
k = find_k(clusters_df, "K", "sel.K")


