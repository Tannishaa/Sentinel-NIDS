# File: brain-engine/fake_sonika.py

import socket
import time

def simulate_dos_attack():
    print("[ATTACKER] Starting Fake SYN Flood DoS Attack...")
    
    # We will send 15 packets rapidly to trigger the >10 threshold in your AI Brain
    for i in range(1, 16):
        try:
            # 1. Create a fresh socket for each packet (mimicking individual connections)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 6000))
            
            # [cite_start]2. The exact CSV Contract you and Sonika agreed on 
            # [cite_start]Format: Source_IP, Destination_Port, Protocol_Name, Size, Flags 
            fake_packet = "192.168.1.5,80,TCP,512,S" 
            
            # 3. Send the data
            client.send(fake_packet.encode('utf-8'))
            print(f"[SENT] Packet {i}/15 fired from 192.168.1.5")
            
            client.close()
            
            # Pause for just a split second so we don't crash our own test
            time.sleep(0.1) 
            
        except ConnectionRefusedError:
            print("[ERROR] Connection Refused. Is Tanisha's inference.py running on Port 6000?")
            break

if __name__ == "__main__":
    simulate_dos_attack()