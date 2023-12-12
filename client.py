import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("An error occurred. Disconnecting...")
            sock.close()
            break

def send_messages(sock):
    while True:
        message = input('')
        try:
            sock.send(message.encode('utf-8'))
        except:
            print("An error occurred. Unable to send the message.")
            sock.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

thread_receiving = threading.Thread(target=receive_messages, args=(client,))
thread_sending = threading.Thread(target=send_messages, args=(client,))

thread_receiving.start()
thread_sending.start()
