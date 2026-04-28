import telnetlib
from datetime import datetime
import getpass

username = input("Username: ")
password = getpass.getpass("Password: ")

devices = [
    {"ip": "192.168.1.10"},
    
]

def backup_device(device):
    print(f"Connecting to {device['ip']}...")

    try:
        tn = telnetlib.Telnet(device["ip"])

        tn.read_until(b"Username:")
        tn.write(username.encode('ascii') + b"\n")

        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")

        tn.write(b"show config\n")   # change if needed
        tn.write(b"exit\n")

        output = tn.read_all().decode('ascii')

        filename = f"{device['ip']}_{datetime.now().strftime('%Y-%m-%d')}.txt"

        with open(filename, "w") as f:
            f.write(output)

        print(f"Backup saved for {device['ip']}")

    except Exception as e:
        print(f"Error with {device['ip']}: {e}")

for device in devices:
    backup_device(device)