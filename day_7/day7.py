import requests, argparse, math
import pandas as pd
from Bio.PDB import *
import matplotlib.pyplot as plt

def fetch_density():
	url = "https://raw.githubusercontent.com/rlabduke/reference_data/master/Top8000/Top8000_ramachandran_pct_contour_grids/rama8000-general-noGPIVpreP.data"
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
			phis += [math.degrees(x[0]) for x in poly.get_phi_psi_list() if None not in x]
			psis += [math.degrees(x[1]) for x in poly.get_phi_psi_list() if None not in x]
	return phis, psis

def plot(phis, psis, densities):
	fig, ax = plt.subplots()
	ax.scatter(phis, psis, s=10)
	cs = ax.tricontour(densities[0], densities[1], densities[2], levels=[0.0005, 0.0200])
	ax.clabel(cs)
	ax.set_xlabel("Φ")
	ax.set_ylabel("Ψ")
	plt.show()

parser = argparse.ArgumentParser(description='Input options to generate ramachandran plot')
parser.add_argument("pdb", help="PDB file or code. If directory, use option -d")
args = parser.parse_args()

pdb_code = args.pdb.strip('.pdb')
download_pdb(pdb_code)
densities = fetch_density()
phis, psis = get_phipsi(pdb_code)
plot(phis, psis, densities)

