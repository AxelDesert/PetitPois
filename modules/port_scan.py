import socket

from modules import utils

def scan_ports():
    utils.print_section_header("LOCAL PORT SCAN")
    try:
        # Try to resolve hostname to IP
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        print(f"Scanning target: {IPAddr} ({hostname})")
    except Exception as e:
        IPAddr = '127.0.0.1'
        print(f"Could not resolve hostname ({e}), scanning 127.0.0.1")

    ports = [21, 22, 23, 53, 80, 123, 139, 161, 443, 445, 3389, 3306, 5432, 5900, 6379, 8080, 27017]
    
    found_any = False
    
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            # connect_ex returns 0 on success
            if s.connect_ex((IPAddr, port)) == 0:
                print(f"Port {port:<5} : {utils.RED}OPEN{utils.RESET}")
                found_any = True
            s.close()
        except:
            pass

    if not found_any:
        print("No open ports found from the common list.")
        
    print("--------------------------------------\n")
