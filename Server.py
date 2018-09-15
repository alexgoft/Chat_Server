# ================IMPORTS======================#
import socket
from threading import Thread
from intro_2_python.chat_server import Client

# ================CONSTANTS======================#

SERVER_WELCOME_MESSAGE = "Welcome! Please enter your nickname:"
SERVER_NAME_TAKEN_MESSAGE = "This nickname is already taken, choose another one:"
OK = "\nYou are logged as {}. You may start chatting"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 658
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)


# =================CLASS=====================#

class Server:

    def __init__(self):

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(ADDRESS)
        self._server_socket.listen(5)

        self._clients = {}

        self._run()

    def client_handler(self, client_socket):
        try:
            client_name = self._establish_new_connection(client_socket)

            while True:
                client_msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
                if client_msg:

                    if client_msg == Client.CLIENT_QUIT_MESSAGE:
                        raise Exception

                    self.broadcast_msg("{}: {}".format(self._clients[client_socket], client_msg))
        except:
            del self._clients[client_socket]
            self.broadcast_msg('{} disconnected.'.format(client_name))

    def _establish_new_connection(self, client_socket):

        # First message exchange - Get name of client and start communication.
        client_socket.send(SERVER_WELCOME_MESSAGE.encode())
        client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        while client_name in self._clients.values():
            client_socket.send(SERVER_NAME_TAKEN_MESSAGE.encode())
            client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        else:
            # Server send OK - communication can be carried out.
            client_socket.send(OK.format(client_name).encode())

        self._clients[client_socket] = client_name

        self.broadcast_msg("{} has connected.".format(client_name), exclude_socket=client_socket)

        return client_name

    def broadcast_msg(self, msg, exclude_socket=None, only_sockets=None):
        # Exclude socket will not receive msg.
        # If only_sockets is not none, only only_sockets will receive msg.

        print(msg)

        iterate_sockets = only_sockets if only_sockets else self._clients
        for sock in iterate_sockets:
            if sock != exclude_socket:
                sock.send(msg.encode())

    def _run(self):
        print('%%% Server is up and running %%%')
        print('%%% Server Address {}:{} %%%'.format(HOST, PORT), '\n')

        threads = []
        while True:
            client_socket, _ = self._server_socket.accept()
            client_thread = Thread(target=self.client_handler, args=(client_socket,))
            client_thread.start()

            threads.append(client_thread)


# =================MAIN=====================#
if __name__ == '__main__':
    server = Server()
