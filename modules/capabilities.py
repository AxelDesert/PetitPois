import subprocess

from modules import utils

def getcap():
    utils.print_section_header("SYSTEM CAPABILITIES (getcap)")
    capabilities = subprocess.run(["getcap", "-r", "/"], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True)
    lines = []
    lenth_filepath = 0
    lenth_caps = 0

    for ligne in capabilities.stdout.splitlines():
        if not ligne.strip(): continue
        try:
            chemin, caps = ligne.rsplit(' ', 1)
            lines.append((chemin, caps))
            
            if len(chemin) > lenth_filepath:
                lenth_filepath = len(chemin)
            if len(chemin) > lenth_caps:
                lenth_caps = len(chemin)
            
        except ValueError:
            continue
            
    padding = lenth_filepath

    print(f"{'FILES':<{padding}} | CAPABILITIES")
    print("-" * (padding + lenth_filepath + lenth_caps))

    for chemin, caps in lines:
        print(f"{chemin:<{padding}} | {utils.RED}{caps}{utils.RESET}")
    print("\n")
