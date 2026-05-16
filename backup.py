import socket
import time
from datetime import datetime
import getpass


username = input("Username: ")
password = getpass.getpass("Password: ")

devices = [
    {"ip": "192.168.2.11"},
]

COMMAND = "show running-config script"


def read_data(sock, delay=2):
    time.sleep(delay)
    data = b""
    sock.setblocking(0)

    try:
        while True:
            part = sock.recv(65535)
            if not part:
                break
            data += part
    except:
        pass

    return data.decode(errors="ignore")


def backup_device(device):
    ip = device["ip"]
    print(f"\n Connecting to {ip}...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 23))

      
        output = read_data(sock, 3)
        print("Initial Output:\n", output)


        if "user" in output.lower():
            sock.send((username + "\n").encode())
            output = read_data(sock, 2)

        
        if "password" in output.lower():
            sock.send((password + "\n").encode())
            output = read_data(sock, 3)

        print("After Login:\n", output)

        
        sock.send(b"\n")
        time.sleep(1)
        sock.send(b"cli\n")
        time.sleep(2)


        print("Sending command...")
        sock.send((COMMAND + "\n").encode())

        
        full_output = ""
        for _ in range(20):  
            full_output += read_data(sock, 1)

       
        filename = f"{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write(full_output)

        print(f" Full backup saved → {filename}")

        sock.close()

    except Exception as e:
        print(f" Error with {ip}: {e}")


for device in devices:
    backup_device(device)

print("\n All backups completed.")
