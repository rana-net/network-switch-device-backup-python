import telnetlib
from datetime import datetime
import getpass
import time

username = input("Enter Username: ")
password = getpass.getpass("Enter Password: ")

devices = [
    {"ip": "192.168.1.10"},
    {"ip": "192.168.1.11"},
]


commands = [
    "show config"
]

def backup_device(device):
    ip = device["ip"]
    print(f"\n Connecting to {ip}...")

    try:
               tn = telnetlib.Telnet(ip, timeout=5)

    
        tn.read_until(b"Username:", timeout=5)
        tn.write(username.encode('ascii') + b"\n")

        tn.read_until(b"Password:", timeout=5)
        tn.write(password.encode('ascii') + b"\n")

        time.sleep(1)  

        output = ""

        for cmd in commands:
            tn.write(cmd.encode('ascii') + b"\n")
            time.sleep(2)  # wait for command output

            cmd_output = tn.read_very_eager().decode('ascii', errors='ignore')
            output += f"\n\n### {cmd} ###\n{cmd_output}"

       
        tn.write(b"exit\n")

       
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{ip}_{timestamp}.txt"

        
        with open(filename, "w") as file:
            file.write(output)

        print(f"Backup saved for {ip} → {filename}")

        tn.close()

    except Exception as e:
        print(f" Error with {ip}: {e}")



for device in devices:
    backup_device(device)

print("\n All backups completed.")
