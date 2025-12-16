import os
from pathlib import Path
import subprocess 


nfs_config_path = '/etc/exports'
nfs_is_active = False

if os.path.isdir(nfs_config_path)==True and Path(nfs_config_path).stat().st_size > 0:
    nfs_is_active = True
    print("NFS Directory exists.")
else:
    nfs_is_active = False
    print("NFS Directory does not exist.")


if nfs_is_active==True:
    print(f"Fichier {nfs_config_path} est actif.")
    print("    Droits actuels :")
    subprocess.run(["ls", "-l", nfs_config_path])