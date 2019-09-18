import pandas as pd
import numpy as np

#Reads in both the expression file and the clusters file we were just playing with
def read_csv(filename, index):
	data = pd.read_csv(filename, index_col=index) 
	return data


def calc_expressions(k_row, exmat_df):
	#create blank dataframe
	k = int(k_row['K'])
	result_df = pd.DataFrame(columns=range(1, k+1), index=exmat_df.index)
	for i in range(1, k+1):
		cells = list(k_row[k_row.columns[k_row.isin([i]).all()]].columns[1:])
		result_df[i] = exmat_df.loc[:,cells].mean(axis=1)
	return result_df

#main
exmat = "E-MTAB-7365.csv" #Single-cell RNA seq expression matrix
clusters = "E-MTAB-7365.clusters.csv"#cell cluster assignments for various values of k

exmat_df = read_csv(exmat, 0)
clusters_df = read_csv(clusters, False)

results_df = calc_expressions(clusters_df[clusters_df['sel.K']], exmat_df)
print(results_df.to_string())


