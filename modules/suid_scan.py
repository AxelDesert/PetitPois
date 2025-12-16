import subprocess
import os

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
             # Try resolving path relative to the main project directory
             # Assuming this module is in project/modules/ and list is in project/
             base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
             candidate = os.path.join(base_dir, 'list_exploitable_bin')
             if os.path.exists(candidate):
                 exploitable_filename = candidate

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
