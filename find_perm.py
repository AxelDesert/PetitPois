import subprocess

ascii_art = r"""
__________        __  .__  __                  .__        
\______   \ _____/  |_|__|/  |_  ______   ____ |__| ______
 |     ___// __ \   __\  \   __\ \____ \ /  _ \|  |/  ___/
 |    |   \  ___/|  | |  ||  |   |  |_> >  <_> )  |\___ \ 
 |____|    \___  >__| |__||__|   |   __/ \____/|__/____  >
               \/                |__|                  \/                          
"""
print(ascii_art)

result = subprocess.run(
    ["find", "/", "-user", "root", "-perm", "-4000", "-type", "f"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)
output = result.stdout

def extract_commands(output):
    lines = output.strip().split('\n')
    commands = [line.split('/')[-1] for line in lines if line]
    return commands

commands = extract_commands(output)
print("Liste des commandes trouvées :")
print(commands)

def parse_exploitable_bin():
    filename = 'list_exploitable_bin'
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    bins = [line.strip() for line in lines if line.strip()]
    return bins
exploitable_bins = parse_exploitable_bin()
print("Liste des binaires exploitables :")
print(exploitable_bins)

def compare_commands_and_bins(output):
    commands = extract_commands(output)
    exploitable_bins = parse_exploitable_bin()
    matches = [cmd for cmd in commands if cmd in exploitable_bins]
    print("Matchs trouvés :")
    print(matches)
compare_commands_and_bins(output)
