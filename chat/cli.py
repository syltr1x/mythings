import socket
import threading
import os
import cypher

global client_ip
# Función para limpiar la pantalla de la terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para imprimir los mensajes recibidos en el formato deseado
def print_messages(messages):
    clear_screen()
    for msg in messages[-12:]:  # Mostrar solo los últimos 10 mensajes
        print(msg)

# Función para recibir mensajes y mostrarlos
def receive_message():
    messages = []
    while True:
        try:
            data = client_socket.recv(1024)
            data = cypher.descifrar_texto('RSA', data)
            messages.append(data)
            print_messages(messages)
            print_input_area()
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

# Función para imprimir el área de entrada de mensajes
def print_input_area():
    print("\n" + "=" * 50)
    print(f"[{client_ip}]> ", end="", flush=True)

# Función para enviar mensajes
def send_message():
    while True:
        message = input()
        if message.lower() == "/exit":
            client_socket.send(cypher.cifrar_texto('RSA', "El usuario ha salido del chat"))
            break
        else:
            message = cypher.cifrar_texto('RSA', message)
            client_socket.send(message)

host = input("Host > ")
port = int(input("Port > "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_ip = client_socket.getsockname()[0]
client_socket.send("#ispassword".encode('utf-8'))
pwdrsp = client_socket.recv(1024).decode('utf-8')
if pwdrsp == "#existpwd":
    password = input("Password >")
    client_socket.send(password.encode('utf-8'))
    accessrsp = client_socket.recv(1024).decode('utf-8')
    if accessrsp == "#granted":
        print("¡Contraseña correcta! Puedes continuar.")
    else:
        print("Contraseña incorrecta. Desconectando.")
        exit()

# Solicitar y enviar el nombre de usuario al servidor
username = input("Ingrese su nombre de usuario: ")
client_socket.send(username.encode('utf-8'))

# Iniciar hilo para recibir mensajes
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Mostrar el área de entrada de mensajes
print_input_area()

# Enviar mensajes en el hilo principal
send_message()

# Cerrar el socket cuando terminemos
client_socket.close()
