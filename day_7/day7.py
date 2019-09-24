import requests, argparse, math
import pandas as pd
from Bio.PDB import *
import matplotlib.pyplot as plt

def fetch_density():
	url = "https://raw.githubusercontent.com/rlabduke/reference_data/master/Top8000/Top8000_ramachandran_pct_contour_grids/rama8000-general-noGPIVpreP.data"
	info = {'phi':[], 'psi':[], 'density':[]}
	r = requests.get(url)
	with open('contour.data', 'w+') as f:
		f.write(r.text)
	densities = pd.read_csv('contour.data', delim_whitespace=True, header=None, comment="#")
	return densities

def download_pdb(pdb_name):
	url = 'https://files.rcsb.org/download/' + pdb_name + '.pdb'
	r = requests.get(url)
	if r.status_code == 200:
		with open(pdb_name + '.pdb', "w+") as f:
			f.write(r.text)
	else:
		print("ERROR: Unable to retrieve pdb file, likely due to incorrect PDB code.")
		sys.exit(-1)

def get_phipsi(pdb_code):
	phis = []
	psis = []
	for model in PDBParser().get_structure(pdb_code, pdb_code + ".pdb") :
		for chain in model:
			poly = Polypeptide.Polypeptide(chain)
			phi_temp = [math.degrees(x[0]) for x in poly.get_phi_psi_list() if None not in x]
			psi_temp = [math.degrees(x[1]) for x in poly.get_phi_psi_list() if None not in x]
			phis += phi_temp
			psis += psi_temp
	return phis, psis

def plot(phis, psis, densities):
	fig, ax = plt.subplots()
	ax.scatter(phis, psis)
	ax.tricontour(densities[0], densities[1], densities[2])
	plt.show()

parser = argparse.ArgumentParser(description='Input options to generate ramachandran plot')
parser.add_argument("pdb", help="PDB file or code. If directory, use option -d")
args = parser.parse_args()

pdb_code = args.pdb.strip('.pdb')
download_pdb(pdb_code)
densities = fetch_density()
phis, psis = get_phipsi(pdb_code)
plot(phis, psis, densities)

