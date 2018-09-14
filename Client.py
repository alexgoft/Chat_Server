from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from intro_2_python.chat_server import Server
import intro_2_python.chat_server.utils as utils

QUIT_MESSAGE = '{quit}'
CLIENTS_MESSAGE = '{clients}'


class Client:

    def __init__(self):
        self._client_socket = socket(AF_INET, SOCK_STREAM)

        self._connect()

    def client_to_server_handler(self):

        # Welcome messages
        print("\nEnter {} to quit session.".format(QUIT_MESSAGE))
        print("Enter {} to get list of clients connected to server.\n".format(CLIENTS_MESSAGE))

        msg = ''
        while msg != QUIT_MESSAGE:
            msg_to_server = input('>> ').encode()
            self._client_socket.send(msg_to_server)

    def _connect(self):

        self._client_socket.connect(Server.ADDRESS)

        print("You are connected to server.", '\n')

        # Handle server communication.
        while True:
            msg_from_server = self._client_socket.recv(Server.BUFFER_SIZE).decode("utf-8")
            print(msg_from_server)

            if msg_from_server == Server.WELCOME_MESSAGE:
                name = input().encode()
                self._client_socket.send(name)

                utils.create_thread_helper(self.client_to_server_handler())


if __name__ == '__main__':
    client = Client()
