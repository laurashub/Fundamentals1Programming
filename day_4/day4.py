import pandas as pd
import numpy as np
import sys, math

#Reads in both the expression file and the clusters file we were just playing with
def read_csv(filename, index):
	data = pd.read_csv(filename, index_col=index) 
	return data


def calc_expressions(k_row, exmat_df):
	k = int(k_row['K'])
	result_df = pd.DataFrame(columns=range(1, k+1), index=exmat_df.index)
	normalized_df = pd.DataFrame(columns=[str(x)+"_dif" for x in range(1, k+1)], index=exmat_df.index)
	for i in range(1, k+1):
		cells = list(k_row.columns[k_row.isin([i]).iloc[0]])[1:]
		result_df[i] = exmat_df.loc[:,cells].mean(axis=1)
		normalized_df[str(i)+"_dif"] = exmat_df.drop(cells, axis=1).mean(axis=1)
		normalized_df[str(i)+"_dif"] = np.log2(result_df[i]/normalized_df[str(i)+"_dif"])
	return pd.concat([result_df, normalized_df], axis=1)

#main
exmat = "E-MTAB-7365.csv" #Single-cell RNA seq expression matrix
clusters = "E-MTAB-7365.clusters.csv"#cell cluster assignments for various values of k

exmat_df = read_csv(exmat, 0)
clusters_df = read_csv(clusters, False)

full_results = calc_expressions(clusters_df[clusters_df['sel.K']], exmat_df)
#diff_df = add_differentials(weights, results_df)
#all_results = pd.concat([results_df, diff_df], axis=1)

print(full_results.to_string())


