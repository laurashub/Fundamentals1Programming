import sys, requests
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

def res_df():
	#http://www.rcsb.org/pdb/rest/customReport.xml?pdbids=*&customReportColumns=structureId,resolution,depositionDate&format=csv
	req = "http://www.rcsb.org/pdb/rest/customReport.csv"
	info={'pdbids': '*',
		'customReportColumns':'resolution,depositionDate',
		'format':'csv'}
	r = requests.get(req, params=info)
	f = StringIO(r.text.replace("<br />", "\n"))
	df = pd.read_csv(f)
	#arrange dates so they plot correctly
	#there probably exists a way to get around this
	df['depositionDate'] = df['depositionDate'].apply(lambda x: int(''.join(c for c in x if c.isdigit())))
	return df

def plot_data(df):
	style.use("ggplot")
	df.plot(kind='scatter',x='depositionDate',y='resolution',color='red')
	plt.show()


plot_data(res_df())