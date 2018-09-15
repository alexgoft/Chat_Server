# ================IMPORTS====================== #
import socket
import re
from threading import Thread
from intro_2_python.chat_server import Client

# ================CONSTANTS====================== #
SERVER_WELCOME_MESSAGE = "Welcome!! Please enter your nickname (Characters and Digits only):"
SERVER_NAME_TAKEN_MESSAGE = "!! This nickname is already taken, choose another one: !!"
OK = "\nYou are logged as {}. You may start chatting"
PUBLIC_MSG = "[PUBLIC] {}: {}"
PRIVATE_MSG = "[PRIVATE] {}->{}: {}"
PRIVATE_MSG_ERR_SELF = "!! Cant send private message: Cant send to yourself !!"
PRIVATE_MSG_ERR_NO_USER = "!! Cant send private message: User does not exists !!"
USER_CONNECTED = "{} has connected."
USER_DISCONNECTED = '{} disconnected.'

# ============================================== #
HOST = socket.gethostbyname(socket.gethostname())
PORT = 658
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)


# =================CLASS===================== #
class Server:

    def __init__(self):

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(ADDRESS)
        self._server_socket.listen(5)

        self._clients_by_name = {}
        self._private_msg_pattern = re.compile("{[0-9a-zA-Z_]+}\s.*")

        self._run()

    def _client_handler(self, client_socket):

        try:
            client_name = self._establish_new_connection(client_socket)

            while True:
                client_msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                if client_msg:

                    if client_msg == Client.CLIENT_QUIT_MESSAGE:
                        raise Exception
                    elif client_msg == Client.CLIENT_CLIENTS_MESSAGE:
                        self._broadcast_msg(self._get_clients_list_str(), only_sockets=[client_socket])
                    elif self._private_msg_pattern.match(client_msg):
                        self._send_private_msg(client_msg, client_name, client_socket)
                    else:
                        self._broadcast_msg(PUBLIC_MSG.format(client_name, client_msg))
        except:
            del self._clients_by_name[client_name]

            self._broadcast_msg(USER_DISCONNECTED.format(client_name))

    def _send_private_msg(self, client_msg, client_name, client_socket):

        client_msg_arr = client_msg.split('{')[1].split('}')

        client_to_contact = client_msg_arr[0]
        private_msg_to_send = client_msg_arr[1][1:]

        if client_to_contact == client_name:
            self._broadcast_msg(PRIVATE_MSG_ERR_SELF, only_sockets=[client_socket])
        elif client_to_contact not in self._clients_by_name.keys():
            self._broadcast_msg(PRIVATE_MSG_ERR_NO_USER, only_sockets=[client_socket])
        else:
            self._broadcast_msg(PRIVATE_MSG.format(client_name, client_to_contact, private_msg_to_send),
                                only_sockets=[client_socket, self._clients_by_name[client_to_contact]])

    def _establish_new_connection(self, client_socket):

        # First message exchange - Get name of client and start communication.
        client_socket.send(SERVER_WELCOME_MESSAGE.encode())

        client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        while client_name in self._clients_by_name.keys():
            client_socket.send(SERVER_NAME_TAKEN_MESSAGE.encode())
            client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        else:
            # Server send OK - communication can be carried out.
            client_socket.send(OK.format(client_name).encode())

        self._clients_by_name[client_name] = client_socket

        self._broadcast_msg(USER_CONNECTED.format(client_name), exclude_socket=client_socket)

        return client_name

    def _get_clients_list_str(self):

        client_names = self._clients_by_name.keys()

        clients_str = '--- Clients ---\n'
        for name in client_names:
            clients_str += name + '\n'
        clients_str += '---------------'

        return clients_str

    def _broadcast_msg(self, msg, exclude_socket=None, only_sockets=None):

        # exclude_socket - socket will not receive msg.
        # only_sockets is not none - only only_sockets will receive msg.

        print(msg)

        iterate_sockets = only_sockets if only_sockets else self._clients_by_name.values()
        for sock in iterate_sockets:
            if sock != exclude_socket:
                sock.send(msg.encode())

    def _run(self):

        print('%%% Server is up and running %%%')
        print('%%% Server Address {}:{} %%%'.format(HOST, PORT), '\n')

        threads = []
        while True:
            client_socket, _ = self._server_socket.accept()
            client_thread = Thread(target=self._client_handler, args=(client_socket,))
            client_thread.start()

            threads.append(client_thread)


# =================MAIN=====================#
if __name__ == '__main__':
    server = Server()
