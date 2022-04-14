import socket

from numpy import array
from Player import Player, deserialize_new_player, deserialize_player


class Connection:
    def __init__(self, server_ip, server_port):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        # connecting to the server
        self.client_socket = socket.socket()
        self.client_socket.settimeout(0.01)
        try:
            self.client_socket.connect((self.SERVER_IP, self.SERVER_PORT))
        except socket.error:
            exit("server offline, init")

    def connect(self) -> Player:
        """connects to the server

        Raises:
            socket.error: the server is offline

        Returns:
            Player: starting player (position, color)
        """
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

    def send_shot(self, color) -> None:
        """sends a shot to the server

        Args:
            color (your color): the color of the player
        """
        try:
            self.client_socket.send(("G" + color).encode())
        except socket.error as e:
            print(e)

    def update_data(self, player: Player) -> array:
        """sending and recieving position updates form the server

        Args:
            player (Player): the player 

        Returns:
            bool, dictionary: true/false is the game over, a list of players with their new positions
            / the score of each player if the game if done
        """
        try:
            # sending our updated data
            # [i] sending and recieving in gl cs
            self.client_socket.send(("P" + player.serialize()).encode())
            # getting other players updated data
            update_data = self.client_socket.recv(1024).decode()
            if update_data.count("F") > 0:
                results = {}
                for player_points in update_data.split("F")[1:]:
                    results[player_points[:-1]] = player_points[-1:]
                return True, results
            else:
                # turning it into a list of players
                update_list = {}
                for player in update_data.split("P")[:-1]:
                    p = deserialize_player(player)
                    if p:
                        update_list[p.color] = p
                return False, update_list
        except socket.error:
            return None, None
            # exit("server offline, updates")

