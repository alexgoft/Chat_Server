# ================IMPORTS======================#

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from intro_2_python.chat_server import Server

# ================CONSTANTS======================#
CLIENT_QUIT_MESSAGE = '{quit}'
CLIENT_CLIENTS_MESSAGE = '{clients}'


# =================CLASS=====================#
class Client:

    def __init__(self):
        self._client_socket = socket(AF_INET, SOCK_STREAM)

        self._connect()

    def client_to_server_handler(self):

        # Welcome messages.
        print('\n====================')
        print("Enter {} to disconnect from the server.".format(CLIENT_QUIT_MESSAGE))
        print("Enter {} to get list of clients connected to server.".format(CLIENT_CLIENTS_MESSAGE))
        print('====================\n')

        # As long as socket is not dead, keep sending messages to server.
        while True:

            msg = input()
            self._client_socket.send(msg.encode())

            # User wish do close the connection.
            if msg == CLIENT_QUIT_MESSAGE:
                self._client_socket.close()
                return

    def server_to_client_handler(self):

        # As long as socket is not dead, keep checking for messages from server.
        while True:

            try:
                msg_from_server = self._client_socket.recv(Server.BUFFER_SIZE).decode("utf-8")
                if msg_from_server:
                    print(msg_from_server)

                    if msg_from_server == Server.SERVER_WELCOME_MESSAGE:
                        name = input().encode()
                        self._client_socket.send(name)

                        # Communication will be possible only after client's initial identification.
                        Thread(target=self.client_to_server_handler, args=()).start()
            except:
                msg = "You disconnected from the server." if self._client_socket.fileno() == -1 else "Connection error."
                print(msg)

                return

    def _connect(self):

        self._client_socket.connect(Server.ADDRESS)

        print("You are connected to server.", '\n')

        # Handle server communication.
        Thread(target=self.server_to_client_handler, args=()).start()


# =================MAIN=====================#

if __name__ == '__main__':
    client = Client()
