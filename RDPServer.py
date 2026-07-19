import socket

# creating the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_host_ip():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return host_ip

my_port = 55001
# bind
server_socket.bind((get_host_ip(), my_port))

# listen
server_socket.listen(1)
print("Waiting for connections")

# accept
connected_socket, address = server_socket.accept()
print(f"connected to {address}")