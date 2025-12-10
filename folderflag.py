import subprocess
import argparse
import time

parser = argparse.ArgumentParser(description="Mini ls en Python")
parser.add_argument("paths", nargs="*", default=["../"], help="Dossier(s) à lister")
parser.add_argument("-l", action="store_true", help="Mode liste détaillée")
parser.add_argument("-f", "--folder", action="store_true", help="Afficher uniquement les dossiers demandés")

args = parser.parse_args()

for path in args.paths:
    files = subprocess.check_output(["ls", path]).decode().splitlines()
    for f in files:
        full_path = f"{path}/{f}" if not path.endswith("/") else f"{path}{f}"

        # Filtrer uniquement les dossiers si --folder
        if args.folder and subprocess.call(["test", "-d", full_path]) != 0:
            continue

        # Afficher les informations selon le mode choisi
        if args.l:
            stats = subprocess.check_output(["stat", "-c", "%s %Y", full_path]).decode().split()
            size = int(stats[0])
            mod_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(stats[1])))
            print(f"{size:>10}  {mod_time}  {full_path}")
        else:
            print(full_path)
