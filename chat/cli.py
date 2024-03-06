import socket
import threading
import os
import cypher

global client_ip
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_messages(messages):
    clear_screen()
    print("=" * 6 + f"Server: {host}=====You: {client_ip}" + "=" * 6)
    for msg in messages[-12:]:
        print(msg)

def receive_message():
    messages = []
    while True:
        try:
            data = client_socket.recv(1024)
            data = cypher.descifrar('RSA', data)
            messages.append(data)
            print_messages(messages)
            print_input_area()
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

def print_input_area():
    print("\n" + "=" * 50)
    print(f"[{client_ip}]> ", end="", flush=True)

def send_message():
    while True:
        message = input()
        if message != "":
            if message.lower() == "/exit":
                client_socket.send(cypher.cifrar('RSA', "El usuario ha salido del chat"))
                break
            else:
                message = cypher.cifrar('RSA', message)
                client_socket.send(message)

host = input("Host > ")
port = int(input("Port > "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_ip = client_socket.getsockname()[0]
client_socket.send(cypher.cifrar('RSA', "#ispassword"))
pwdrsp = client_socket.recv(1024)
pwdrsp = cypher.descifrar('RSA', pwdrsp)
if pwdrsp == "#existpwd":
    password = input("Password >")
    client_socket.send(cypher.cifrar('RSA', password))
    accessrsp = client_socket.recv(1024)
    accessrsp = cypher.descifrar('RSA', accessrsp)
    if accessrsp == "#granted":
        print("¡Contraseña correcta! Puedes continuar.")
    else:
        print("Contraseña incorrecta. Desconectando.")
        exit()

username = input("Ingrese su nombre de usuario: ")
client_socket.send(cypher.cifrar('RSA', username))
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

print_input_area()
send_message()
client_socket.close()