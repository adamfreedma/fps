import socket
import select

from Player import Player


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
                print(msg)
                client_socket.send(msg.encode())
                messages.remove(message)
            except Exception as e:
                handle_disconnected_client(client_socket)
                message_to_send_cleared = [m for m in messages if m[0] is client_socket]
                messages = message_to_send_cleared


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1729))
server_socket.listen(5)

# clients
open_client_sockets = {}
message_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + list(open_client_sockets.keys()), [server_socket] + list(open_client_sockets.keys()), [])

    for curr_socket in rlist:
        if curr_socket is server_socket:
            (new_client, address) = server_socket.accept()
            print(f'{address[0]}, connected to the server')
            open_client_sockets[new_client] = address[0]
        else:
            data = ""
            try:
                data = curr_socket.recv(1024).decode()
            except Exception as e:
                print(str(e))
                handle_disconnected_client(curr_socket)

            if data == "":
                handle_disconnected_client(curr_socket)
            else:
                print(data)
                if data == "J":
                    # TODO: change to actual values
                    message = "S" + "2".zfill(30) + "black"
                    message_to_send.append((curr_socket, message))
                else:
                    for target_socket in wlist:
                        if target_socket is not curr_socket:
                            message_to_send.append((target_socket, data))
        
        for curr_socket in wlist:
            message_to_send.append((curr_socket, "P" + Player("red", [10,0,0]).serialize()))


    send_waiting_messages(wlist, message_to_send)
