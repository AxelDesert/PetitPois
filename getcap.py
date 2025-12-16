import subprocess
import os

def getcap():
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

    print("Result of getcap since root :\n")
    print(f"{'FILES':<{padding}} | CAPABILITIES")
    print("-" * (padding + lenth_filepath + lenth_caps))

    for chemin, caps in lines:
        print(f"{chemin:<{padding}} | {caps}")
    print("\n")


def whoami():
    RED = "\033[31m"
    RESET = "\033[0m"

    def run_cmd(cmd):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except Exception as e:
            return "", str(e), -1

    stdout_user, stderr_user, code_user = run_cmd(["whoami"])
    stdout_id, stderr_id, code_id = run_cmd(["id"])
    stdout_groups, stderr_groups, code_groups = run_cmd(["groups"])

    print(" ")
    print(f"{RED}whoami:{RESET}", f"{stdout_user}{RESET}")
    print(" ")
    print(f"{RED}id:{RESET}", f"{stdout_id}{RESET}")
    print(" ")
    print(f"{RED}groups:{RESET}", f"{stdout_groups}{RESET}")

    is_root = (os.geteuid() == 0)
    if is_root:
        print(f"{RED}Exécution en tant que root.{RESET}")
    else:
        print(f"{RED}Exécution sans privilèges élevés.{RESET}")
    print()
    
    groups = stdout_groups.split()
    if "sudo" in groups:
        print(f"{RED}L'utilisateur est dans le groupe sudo.{RESET}")
    else:
        print(f"{RED}Utilisateur sans accès sudo.{RESET}")
    if "docker" in groups:
        print(f"{RED}L'utilisateur est dans le groupe docker. {RESET}")
    else:
        print(f"{RED}Utilisateur sans accès docker.{RESET}")


def find_suid_exploits():
    print("\n--- Scanning for SUID Binaries ---")
    try:
        # Run find command
        cmd = ["find", "/", "-user", "root", "-perm", "-4000", "-type", "f"]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        output = result.stdout
        
        # Parse output, filter /snap/, and keep full paths
        lines = output.strip().split('\n')
        # List of tuples: (full_path, binary_name)
        found_suids = [(line, line.split('/')[-1]) for line in lines if line and not line.startswith('/snap/')]
        
        print(f"Found {len(found_suids)} SUID binaries (excluding /snap/).")

        # Load exploitable list
        exploitable_filename = 'list_exploitable_bin'
        if not os.path.exists(exploitable_filename):
             # Try absolute path based on script location if relative fails
             script_dir = os.path.dirname(os.path.abspath(__file__))
             exploitable_filename = os.path.join(script_dir, 'list_exploitable_bin')

        if os.path.exists(exploitable_filename):
            with open(exploitable_filename, 'r') as f:
                content = f.read().strip().split('\n')
            exploitable_names = set([line.strip() for line in content if line.strip()])
            
            # Match
            matches = [path for path, name in found_suids if name in exploitable_names]
            
            if matches:
                 print("\n\033[31m[!] POTENTIALLY EXPLOITABLE SUID BINARIES FOUND:\033[0m")
                 for match in matches:
                     print(f"    {match}")
            else:
                print("\nNo known exploitable SUID binaries found from the list.")
        else:
            print(f"\nWarning: Could not find '{exploitable_filename}'. Skipping exploit check.")
            print("Here are the SUID binaries found:")
            for path, name in found_suids:
                print(path)

    except Exception as e:
        print(f"Error during SUID scan: {str(e)}")
    print("----------------------------------\n")


if __name__ == "__main__":
    print("--- SCRIPT ---")
    print("1. GETCAP")
    print("2. WHOAMI")
    print("3. FIND SUID (New)")
    print("4. ALL")
    
    choix = input("\nVotre choix : \n")

    if choix == "1":
        getcap()
    elif choix == "2":
        whoami()
    elif choix == "3":
        find_suid_exploits()
    elif choix == "4":
        getcap()
        whoami()
        find_suid_exploits()