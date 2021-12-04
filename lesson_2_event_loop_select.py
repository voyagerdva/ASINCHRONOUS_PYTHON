# ASINCHRONOUS_PYTHON
import socket
from select import select

PORT = 5001
ADDRESS = "localhost"
to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((ADDRESS, PORT))
server_socket.listen()


def accept_connection(server_socket):
    print(f"Server is started on {PORT}")
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)
    to_monitor.append(client_socket)

def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        response = "Hello world\n".encode()
        client_socket.send(response)
    else:
        client_socket.close()


def event_loop():
    while True:

        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)




if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()