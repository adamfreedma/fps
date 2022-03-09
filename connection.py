import socket
from sys import int_info
from turtle import up
from Player import deserialize_new_player, deserialize_player

class Connection:
    def __init__(self, server_ip, server_port):
        self.SERVER_IP =  server_ip
        self.SERVER_PORT = server_port
        # connecting to the server
        self.client_socket = socket.socket()
        self.client_socket.settimeout(0.1)
        try:
            self.client_socket.connect((self.SERVER_IP, self.SERVER_PORT))
        except socket.error:
            exit("server offline, init")

    def connect(self):
        try:
            self.client_socket.send("J".encode())
            init_data = self.client_socket.recv(1024).decode()
            if len(init_data) < 1 or init_data[0] != "S":
                raise socket.error
            return deserialize_new_player(init_data[1:])
        except socket.error:
            exit("server offline, connect")
    
    def send_movement(self, player):
        try:
            self.client_socket.send(("P" + player.serialize()).encode())
        except socket.error:
            exit("server offline, send movement")


    def recv_updates(self):
        try:
            update_data = self.client_socket.recv(1024).decode()
            if update_data[0] == "H":
                return update_data[0:], None
            elif update_data[0] == "P":
                p = deserialize_player(update_data[0:])
                return p.color. p
        except socket.error:
            exit("server offline, recv updates")

