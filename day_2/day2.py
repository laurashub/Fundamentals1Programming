import requests
import tarfile
import sys, os

def download_tar(tar_base, tar_name, target_path):
	if os.path.isfile(target_path):
		print("File already downloaded")
	else:
		print("Requesting file...")
		r = requests.get(tar_base + "/" + tar_name, stream=True)
		if r.status_code == 200:
			with open(target_path, 'wb') as f:
				f.write(r.raw.read())
			print("File downloaded successfully!")
		else:
			print("Error retrieving tar file: " + str(r.status_code))
			sys.exit(-1)

def unpack_tar(target_path):
	pdb_names = set()
	tf = tarfile.open(name=target_path)
	for name in tf.getnames()[1:]:
		n = name.split("/")[-1][0:4] #only get 4 letter pdb code
		pdb_names.add(n)
	return pdb_names

def print_names(pdb_names):
	for name in sorted(list(pdb_names)):
		print(name)

# http://www.rbvi.ucsf.edu/Outreach/PythonBootCamp2019/modules/oop/top500H.tgz

base = "http://www.rbvi.ucsf.edu/Outreach/PythonBootCamp2019/modules/oop/"
tar_name = "top500H.tgz"
tar_path = "top500H.tgz"

download_tar(base, tar_name, tar_path)
pdb_names = unpack_tar(tar_path)
print_names(pdb_names)

