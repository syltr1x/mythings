import socket
import threading
import random as r
import cypher
from colorama import Fore as c, init
init()
clients = {}
password, epwd = "1234", True

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            data = cypher.descifrar('RSA', data)
            if not data:
                print(f"{c.RED}[*] {clients[client_socket]} se ha desconectado.{c.WHITE}")
                del clients[client_socket]
                break
            if data.startswith("/chname"):
                new_username = data.split(" ")[1]
                old_username = clients[client_socket]
                clients[client_socket] = new_username
                print(f"[*] {old_username} cambió su nombre a {new_username}.")
                send_to_all_except(client_socket, f"[*] {old_username} cambió su nombre a {new_username}.")
            elif data.startswith('/users'):
                send_only_one(client_socket, f"{c.YELLOW}[Server] > {len(clients)} Users Connected.{c.WHITE}" if len(clients) > 1 else f"{c.YELLOW}[Server] > {len(clients)} User Connected.{c.WHITE}")
            else:
                sender_username = clients[client_socket]
                print(f"[{sender_username}] > {data}")
                send_to_all(f"[{sender_username}] > {data}".strip())
        except:
            print(f"[*] Error al recibir datos del cliente {clients[client_socket]}.")
            del clients[client_socket]
            break

def send_only_one(sended_socket, message):
    message = cypher.cifrar('RSA', message)
    for client_socket in clients:
        if client_socket == sended_socket:
            try:
                client_socket.send(message)
            except:
                print(f"[*] Error al enviar mensaje.")
            
def send_to_all(message):
    message = cypher.cifrar('RSA', message)
    for client_socket in clients:
        try:
            client_socket.send(message)
        except:
            print(f"[*] Error al enviar mensaje.")

def send_to_all_except(sender_socket, message):
    message = cypher.cifrar('RSA', message)
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                print(f"[*] Error al enviar mensaje.")

def main():
    host = input("Host > ")
    port = r.randint(5000, 10000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Servidor escuchando en {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Cliente {client_address} conectado.")
        received_request = client_socket.recv(1024)
        received_request = cypher.descifrar('RSA', received_request)
        if received_request == "#ispassword":
            if epwd == True:
                client_socket.send(cypher.cifrar('RSA', '#existpwd'))
                received_password = client_socket.recv(1024)
                received_password = cypher.descifrar('RSA', received_password)
                if received_password == password:
                    client_socket.send(cypher.cifrar('RSA', "#granted"))
                else:
                    client_socket.send(cypher.cifrar('RSA', "#blocked"))
            else: 
                client_socket.send(cypher.cifrar('RSA', "#nexistpwd"))
        
        username = client_socket.recv(1024)
        username = cypher.descifrar('RSA', username)
        clients[client_socket] = username
        send_to_all_except(client_socket, f"{c.GREEN}[*] {username} se ha conectado.{c.WHITE}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()