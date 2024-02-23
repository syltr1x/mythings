import socket
import threading

def send_message():
    while True:
        message = input("> ")
        if message.startswith("/chname "):
            new_username = message.split(" ")[1]
            client_socket.send(f"CHANGENAME {new_username}".encode('utf-8'))
        else:
            client_socket.send(message.encode('utf-8'))

host = "127.0.0.1"
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Solicitar y enviar el nombre de usuario al servidor
username = input("Ingrese su nombre de usuario: ")
client_socket.send(username.encode('utf-8'))

send_thread = threading.Thread(target=send_message)
send_thread.start()

while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        print("[*] Servidor desconectado.")
        break
    print(data)

