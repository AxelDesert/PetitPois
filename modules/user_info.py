import subprocess
import os

from modules import utils

def whoami():
    utils.print_section_header("CURRENT USER INFORMATION")
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
    print(f"whoami: {stdout_user}")
    print(" ")
    print(f"id: {stdout_id}")
    print(" ")
    print(f"groups: {stdout_groups}")

    is_root = (os.geteuid() == 0)
    if is_root:
        print(f"{utils.RED}Exécution en tant que root.{utils.RESET}")
    else:
        print(f"Exécution sans privilèges élevés.")
    print()
    
    groups = stdout_groups.split()
    if "sudo" in groups:
        print(f"{utils.RED}L'utilisateur est dans le groupe sudo.{utils.RESET}")
    else:
        print(f"Utilisateur sans accès sudo.")
    if "docker" in groups:
        print(f"{utils.RED}L'utilisateur est dans le groupe docker.{utils.RESET}")
    else:
        print(f"Utilisateur sans accès docker.")
