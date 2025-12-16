from modules import capabilities
from modules import user_info
from modules import suid_scan

if __name__ == "__main__":
    ascii_art = r"""
__________        __  .__  __                  .__        
\______   \ _____/  |_|__|/  |_  ______   ____ |__| ______
 |     ___// __ \   __\  \   __\ \____ \ /  _ \|  |/  ___/
 |    |   \  ___/|  | |  ||  |   |  |_> >  <_> )  |\___ \ 
 |____|    \___  >__| |__||__|   |   __/ \____/|__/____  >
               \/                |__|                  \/
"""
    print(ascii_art)
    print("--- PETIT POIS ---")
    print("1. GETCAP")
    print("2. WHOAMI")
    print("3. FIND SUID")
    print("4. ALL")
    
    try:
        choix = input("\nVotre choix : ")

        if choix == "1":
            capabilities.getcap()
        elif choix == "2":
            user_info.whoami()
        elif choix == "3":
            suid_scan.find_suid_exploits()
        elif choix == "4":
            capabilities.getcap()
            user_info.whoami()
            suid_scan.find_suid_exploits()
        else:
            print("Invalid Option")
    except KeyboardInterrupt:
        print("\nExiting...")
