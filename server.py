import socket
import select
import server_objects
import Player
from random import randint
from time import time

class Game:

    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 1729))
        self.server_socket.listen(5)

        self.points = {}
        self.socket_colors = {}
        self.color_list = {"green": True, "red": True, "blue": True}
        self.player_list = {}
        # saving death times to stop killing respawning people
        self.death_times = {}
        # clients
        self.open_client_sockets = {}
        self.message_to_send = []

        self.RESPAWN_TIME = 5
        self.POINTS_TO_WIN = 9

    def _disconnect_all_clients(self) -> None:
        """disconnects akk connected client sockets
        """
        for client_socket in self.open_client_sockets:
            client_socket.close()
        self.player_list = {}
        self.socket_colors = {}
        self.open_client_sockets = {}

    def _handle_disconnected_client(self, client_socket : socket.socket) -> None:
        """disconnects a single socket and removes it from lists he is in

        Args:
            client_socket (socket): socket to disconnect
        """
        try:
            if client_socket in self.open_client_sockets:
                self.color_list[self.socket_colors[client_socket]] = True
                del self.player_list[self.socket_colors[client_socket]]
                del self.socket_colors[client_socket]
                print(f'{self.open_client_sockets[client_socket]} - disconnected')
                del self.open_client_sockets[client_socket]
                client_socket.close()
        except Exception as e:
            print(e)

    def _reset_vars(self) -> None:
        """resets all vars that are game specific
        """
        self.points = {}
        self.color_list = {"green": True, "red": True, "blue": True}
        self.death_times = {}

    def _send_waiting_messages(self, wlist, messages) -> None:
        """sends all messages that are currently in the message queue

        Args:
            wlist (list of sockets): sockets that are ready to write to
            messages (list of (socket, str)): messages to send
        """
        for message in messages:
            client_socket, msg = message
            if client_socket in wlist:
                try:
                    client_socket.send(msg.encode())
                    messages.remove(message)
                except Exception as e:
                    self._handle_disconnected_client(client_socket)
                    message_to_send_cleared = [m for m in messages if m[0] is client_socket]
                    messages = message_to_send_cleared

    def play(self) -> None:
        """main loop
        """
        while True:
            r_list, w_list, x_list = select.select([self.server_socket] + list(self.open_client_sockets.keys()), [self.server_socket] + list(self.open_client_sockets.keys()), [])

            for curr_socket in r_list:
                # checking for new connections
                if curr_socket is self.server_socket:
                    (new_client, address) = self.server_socket.accept()
                    print(f'{address[0]}, connected to the server')
                    self.open_client_sockets[new_client] = address[0]
                else:
                    try:
                        # getting input data
                        input_data = curr_socket.recv(1024).decode()
                    except Exception as e:
                        print(str(e))
                        self._handle_disconnected_client(curr_socket)

                    if input_data == "":
                        self._handle_disconnected_client(curr_socket)

                    for data in input_data.split("%")[1:]:
                        if data == "J":
                            c = ""
                            for color, available in self.color_list.items():
                                if available:
                                    c = color
                                    self.color_list[color] = False
                                    self.socket_colors[curr_socket] = c
                                    break
                            # TODO: generate random starting position
                            message = "S" + "2".zfill(30) + c
                            self.message_to_send.append((curr_socket, message))
                        elif data[0] == "G":
                            player = Player.deserialize_player(self.player_list[data[1:]])
                            hit = server_objects.line_world_intersection(player.position, player.looking_vector(), data[1:])
                            if hit and (hit not in self.death_times or time() - self.death_times[hit] > self.RESPAWN_TIME):
                                self.player_list[hit] = player.serialize()[:50]
                                self.death_times[hit] = time()
                                self.points[self.socket_colors[curr_socket]] += 1
                                for target_socket in w_list:
                                    self.message_to_send.append((target_socket, self.player_list[hit] + hit + "P"))

                                # sending game results to players
                                if self.points[self.socket_colors[curr_socket]] >= self.POINTS_TO_WIN:
                                    message = ""
                                    # sorting the self.points list from most self.points to least
                                    self.points = {k: v for k, v in sorted(self.points.items(), key=lambda item: item[1], reverse=True)}
                                    self.message_to_send = []
                                    for key, val in self.points.items():
                                        message += "F" + key + str(val).zfill(1)

                                    for target_socket in w_list:
                                        self.message_to_send.append((target_socket, message))
                                    self._send_waiting_messages(w_list, self.message_to_send)
                                    self._reset_vars()

                        elif data[0] == "P":
                            update_list = data.split("P")[1:]
                            for player_data in update_list:
                                if len(player_data) > 50:
                                    color = player_data[50:]
                                    # [i] position in gl cs
                                    value = player_data[:50]
                                    self.player_list[color] = value
                                    if color not in self.points:
                                        self.points[color] = 0
                                    server_objects.create_player(color, Player.deserialize_player(value).position)
                            message = ""
                            for key, val in self.player_list.items():
                                if key != color:
                                    message += val + key + "P"
                            self.message_to_send.append((curr_socket, message))

            self._send_waiting_messages(w_list, self.message_to_send)


def main() -> None:
    """ game init
    """
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
