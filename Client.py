from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from intro_2_python.chat_server import Server

CLIENT_QUIT_MESSAGE = '{quit}'
CLIENT_CLIENTS_MESSAGE = '{clients}'


class Client:

    def __init__(self):
        self._client_socket = socket(AF_INET, SOCK_STREAM)

        self._connect()

    def client_to_server_handler(self):

        # Welcome messages
        print('\n====================')
        print("Enter {} to quit session.".format(CLIENT_QUIT_MESSAGE))
        print("Enter {} to get list of clients connected to server.".format(CLIENT_CLIENTS_MESSAGE))
        print('====================\n')

        while True:
            msg = input().encode()
            if msg == CLIENT_QUIT_MESSAGE:
                break
            self._client_socket.send(msg)

    def server_to_client_handler(self):

        while True:
            msg_from_server = self._client_socket.recv(Server.BUFFER_SIZE).decode("utf-8")
            if msg_from_server:
                print(msg_from_server)

                if msg_from_server == Server.SERVER_WELCOME_MESSAGE:
                    name = input().encode()
                    self._client_socket.send(name)

                    Thread(target=self.client_to_server_handler, args=()).start()

    def _connect(self):

        self._client_socket.connect(Server.ADDRESS)

        print("You are connected to server.", '\n')

        # Handle server communication.
        Thread(target=self.server_to_client_handler, args=()).start()


if __name__ == '__main__':
    client = Client()
