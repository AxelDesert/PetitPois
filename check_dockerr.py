import docker

RED = "\033[91m"
GREEN = "\033[92m"
ORANGE = "\033[93m"
RESET = "\033[0m"

def check_elevated_privileges():
    client = docker.from_env()
    containers = client.containers.list()

    print(f"Audit des privilèges sur {len(containers)} conteneur(s)...\n")

    for container in containers:
        cfg = container.attrs
        host_cfg = cfg['HostConfig']
        name = container.name
        is_secure = True
        if host_cfg['Privileged']:
            print(f"  {RED}[DANGER] Mode PRIVILEGED activé !{RESET}")
            print(f"     -> Le conteneur a accès à tous les périphériques de l'hôte.")
            is_secure = False
        caps = host_cfg.get('CapAdd')
        if caps:
            print(f"  {ORANGE}[WARN] Capabilities Linux ajoutées : {caps}{RESET}")
            if 'SYS_ADMIN' in caps:
                print(f"     -> {RED}SYS_ADMIN détecté !{RESET} (Équivalent à root sur l'hôte)")
            if 'NET_ADMIN' in caps:
                print(f"NET_ADMIN détecté")
            is_secure = False
        app_armor = cfg.get('AppArmorProfile')
        if app_armor == 'unconfined':
             print(f"AppArmor est désactivé")
             is_secure = False
        user = cfg['Config']['User']
        if user == '' or user == '0' or user == 'root':
             print(f"Le processus tourne en tant que ROOT (UID 0)")
        if is_secure:
            print(f"Aucun privilège excessif détecté.")
        
        print("-" * 50)

if __name__ == "__main__":
    check_elevated_privileges()