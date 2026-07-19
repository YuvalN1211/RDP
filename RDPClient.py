import socket

# creating the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_host_ip():
    host_name = "yuvals_leptop"
    host_ip = socket.gethostbyname(host_name)
    return host_ip

my_port = 55001
# connect
client_socket.connect((get_host_ip(), my_port))