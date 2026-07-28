# dependencies
import socket
import keyboard
import threading
import win32api
import time

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



FPS = 30 # also the amount of times the mouse pos is sent in a second

def send_to_server(encoded_msg):
    print(f"sending: {encoded_msg}")
    connected_socket.send(encoded_msg)

msg_size_in_bytes = 16

def create_keyboard_msg(event):
    button = event.name
    encoded_button = ("K" + button.zfill(msg_size_in_bytes-1)).encode()
    print(encoded_button)
    
def keyboard_listen():
    keyboard.on_press(callback=create_keyboard_msg)
    keyboard.wait(hotkey="esc")


def create_mouse_msg(event, data):
    if event == "pos":
        encoded_data = ("MP" + data.zfill(msg_size_in_bytes-2)).encode()
        
    elif event == "click":
        encoded_data = (data.zfill(msg_size_in_bytes)).encode()

    send_to_server(encoded_data)

def mouse_listen():
    while True:
        time.sleep(1 / FPS)
        mouse_action = check_if_mouse_button_pressed()
        print(mouse_action)
        if not mouse_action:
            x, y = win32api.GetCursorPos()
            create_mouse_msg("pos", f"X{x}Y{y}")
        else:
            create_mouse_msg("click", mouse_action)

def check_if_mouse_button_pressed():
    LEFT_BUTTON = 0x01
    RIGHT_BUTTON = 0x02
    MIDDLE_BUTTON = 0x04

    if win32api.GetAsyncKeyState(LEFT_BUTTON) < 0:
        return "ML"
        
    if win32api.GetAsyncKeyState(RIGHT_BUTTON) < 0:
        return "MR"
        
    if win32api.GetAsyncKeyState(MIDDLE_BUTTON) < 0:
        return "MM"
    return


keyboard_thread = threading.Thread(target=keyboard_listen)
mouse_thread = threading.Thread(target=mouse_listen)

keyboard_thread.start()
mouse_thread.start()

keyboard_thread.join()
mouse_thread.join()
print("this is the end")
