import socket
import select
import server_objects
import Player
from random import randint
from time import time

def handle_disconnected_client(client_socket):
    if client_socket in open_client_sockets:
        print(f'{open_client_sockets[client_socket]} - disconnected')
        del open_client_sockets[client_socket]
        client_socket.close()


def send_waiting_messages(wlist, messages):
    for message in messages:
        client_socket, msg = message
        if client_socket in wlist:
            try:
                client_socket.send(msg.encode())
                messages.remove(message)
            except Exception as e:
                handle_disconnected_client(client_socket)
                message_to_send_cleared = [m for m in messages if m[0] is client_socket]
                messages = message_to_send_cleared


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1729))
server_socket.listen(5)
c = "red"
color_list = ["black", "green", "red", "blue"]
player_list = {}
# saving death times to stop killing respawning people
death_times = {}
# clients
open_client_sockets = {}
message_to_send = []

RESPAWN_TIME = 5

while True:
    r_list, w_list, x_list = select.select([server_socket] + list(open_client_sockets.keys()), [server_socket] + list(open_client_sockets.keys()), [])

    for curr_socket in r_list:
        # checking for new connections
        if curr_socket is server_socket:
            (new_client, address) = server_socket.accept()
            print(f'{address[0]}, connected to the server')
            open_client_sockets[new_client] = address[0]
        else:
            data = ""
            try:
                # getting input data
                data = curr_socket.recv(1024).decode()
            except Exception as e:
                print(str(e))
                handle_disconnected_client(curr_socket)
            if data == "":
                handle_disconnected_client(curr_socket)
            else:
                if data == "J":
                    # TODO: change to actual values
                    message = "S" + "2".zfill(30) + c
                    c = "green"
                    message_to_send.append((curr_socket, message))
                elif data[0] == "G":
                    player = Player.deserialize_player(player_list[data[1:]])
                    hit = server_objects.line_world_intersection(player.position, player.looking_vector(), data[1:])
                    if hit and (hit not in death_times or time() - death_times[hit] > RESPAWN_TIME):
                        print("hit")
                        player.move_to(x=randint(-10, 10), z=randint(-10, 10))
                        player_list[hit] = player.serialize()[:50]
                        death_times[hit] = time()
                        for target_socket in w_list:
                            message_to_send.append((target_socket, player_list[hit] + hit + "P"))
                elif data[0] == "P":
                    update_list = data.split("P")[1:]
                    for player_data in update_list:
                        if len(player_data) > 50:
                            color = player_data[50:]
                            # [i] position in gl cs
                            value = player_data[:50]
                            player_list[color] = value
                            server_objects.create_player(color, Player.deserialize_player(value).position)
                    message = ""
                    for key, val in player_list.items():
                        if key != color:
                            message += val + key + "P"
                    message_to_send.append((curr_socket, message))

    send_waiting_messages(w_list, message_to_send)
