import sys

#Reads in both the expression file and the clusters file we were just playing with
def read_file(filename, sep_header = False):
	data = {}
	for i, line in enumerate(open(filename)):
		if sep_header and i == 0:
			header = line.split(',')
		else:
			(gene, expr) = line.split(',',1)
			data[gene] = expr.split(',')
	if sep_header:
		return header, data
	return data

"""
For the default value of k (noted by the True in the first column of the clusters file) 
"""
def cluster_cells(cell_list):
	cells = cell_list['"sel.K"'][1:]
	clusters = {1:[], 2:[], 3:[], 4:[], 5:[]}
	for i, cell in enumerate(cells):
		clusters[int(cell_list['True'][i+1])].append(cell.strip('\n'))
	return (clusters)

"""
calculate the average expression for each gene within each cluster
"""
def cluster_indices(cells, clusters):
	index_clusters = {1:[], 2:[], 3:[], 4:[], 5:[]}
	for i, cell in enumerate(cells):
		for cluster in range(1, 6):
			if cell in clusters[cluster]:
				index_clusters[cluster].append(i)
	return index_clusters

#gene: name

def average_expression(cluster, gene, expression):
	exp = expression[gene]
	avg_exp = 0
	num_exp = 0
	for i in cluster:
		if exp[i] != '':
			avg_exp += float(exp[i])
			num_exp += 1
	if num_exp == 0:
		return "N/A"
	return avg_exp/num_exp

def calc_expressions(index_clusters, exmat_df):
	gene_expression = {}
	for cluster in index_clusters.keys():
		gene_expression[cluster] = {}
		for gene in exmat_df.keys():
			gene_expression[cluster][gene] = average_expression(index_clusters[cluster], gene, exmat_df)
	return gene_expression

def print_results(df, expression):
	for gene in df.keys():
		print(gene + ":", end=" ")
		for i in range(1,6):
			if expression[i][gene] == "N/A":
				print ("N/A", end=' ')
			else:
				print("{0:.3f}".format(expression[i][gene]), end=" ")
		print()

#main
exmat = "E-MTAB-7365.csv" #Single-cell RNA seq expression matrix
clusters = "E-MTAB-7365.clusters.csv"#cell cluster assignments for various values of k

#read files, gen clusters
clusters = cluster_cells(read_file(clusters))
header, exmat_df = read_file(exmat, True)
index_clusters = cluster_indices(header, clusters)

#calc expression
gene_expression=calc_expressions(index_clusters, exmat_df)

#print
print_results(exmat_df, gene_expression)

