import socket
import threading

# Diccionario para mapear nombres de usuario con sus sockets
clients = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"[*] Cliente {clients[client_socket]} desconectado.")
                del clients[client_socket]  # Eliminar cliente del diccionario
                break
            if data.startswith("CHANGENAME "):
                new_username = data.split(" ")[1]
                old_username = clients[client_socket]
                clients[client_socket] = new_username
                print(f"[*] Cliente {old_username} cambió su nombre a {new_username}.")
                send_to_all_except(client_socket, f"[*] {old_username} cambió su nombre a {new_username}.")
            else:
                sender_username = clients[client_socket]
                print(f"{sender_username}: {data}")
                send_to_all_except(client_socket, f"{sender_username}: {data}")
        except:
            print(f"[*] Error al recibir datos del cliente {clients[client_socket]}.")
            del clients[client_socket]  # Eliminar cliente del diccionario
            break

def send_to_all_except(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                print(f"[*] Error al enviar mensaje al cliente {clients[client_socket]}.")

def main():
    host = "127.0.0.1"
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Servidor escuchando en {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Cliente {client_address} conectado.")
        
        # Solicitar y registrar el nombre de usuario
        client_socket.send("Ingrese su nombre de usuario: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        
        # Enviar mensaje de bienvenida a todos los clientes
        send_to_all_except(client_socket, f"[*] ¡Bienvenido {username} al chat!")

        # Iniciar un hilo para manejar la comunicación con el cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()

