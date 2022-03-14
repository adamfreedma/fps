import socket
from Player import Player, deserialize_new_player, deserialize_player

class Connection:
    def __init__(self, server_ip, server_port):
        self.SERVER_IP =  server_ip
        self.SERVER_PORT = server_port
        # connecting to the server
        self.client_socket = socket.socket()
        self.client_socket.settimeout(0.01)
        try:
            self.client_socket.connect((self.SERVER_IP, self.SERVER_PORT))
        except socket.error:
            exit("server offline, init")

    def connect(self):
        try:
            # send J (asking for connection)
            self.client_socket.send("J".encode())
            # getting initial position
            init_data = self.client_socket.recv(1024).decode()
            # rasing a socket error if its invlaid
            if len(init_data) < 1 or init_data[0] != "S":
                raise socket.error
            return deserialize_new_player(init_data[1:])
        except socket.error:
            exit("server offline, connect")
    

    def update_data(self, player):
        try:
            # sending our updated data
            # [i] sending and recieving in gl cs
            self.client_socket.send(("P" + player.serialize()).encode())
            # getting other players updated data
            update_data = self.client_socket.recv(1024).decode()
            # turning it into a list of players
            update_list = {}
            for player in update_data.split("P")[:-1]:
                p = deserialize_player(player)
                if p:
                    update_list[p.color] = p
            return update_list
        except socket.error:
            return None
            # exit("server offline, updates")

