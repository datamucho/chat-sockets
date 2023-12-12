import socket
import threading

clients = []
names = {}

def handle_client(client_socket):
    name = names[client_socket]
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                formatted_message = f"{name}: {message}"
                print(formatted_message)  # Server prints the message
                broadcast_message(formatted_message, client_socket)
            else:
                break
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    del names[client_socket]
    broadcast_message(f"{name} has left the chat.")

def broadcast_message(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                client_name = names[client]
                del names[client]
                broadcast_message(f"{client_name} has left the chat.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen()

print("Server is listening...")

def receive_input():
    while True:
        message = input('')
        broadcast_message("Server: " + message)

thread = threading.Thread(target=receive_input)
thread.start()

while True:
    client_socket, addr = server.accept()
    client_socket.send("Enter your name:".encode('utf-8'))
    client_name = client_socket.recv(1024).decode('utf-8')
    names[client_socket] = client_name
    clients.append(client_socket)
    print(f"{client_name} has joined the chat.")
    broadcast_message(f"{client_name} has joined the chat.")
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
