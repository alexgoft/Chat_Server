# ================IMPORTS====================== #
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from intro_2_python.chat_server import Server

# ================CONSTANTS====================== #
CLIENT_QUIT_MESSAGE = '{quit}'
CLIENT_CLIENTS_MESSAGE = '{clients}'
DISCONNECT_MSG = "You disconnected from the server."
CONNECTION_ERR = "Connection error."
START_CHATTING = "You may start chatting"


# =================CLASS===================== #
class Client:

    def __init__(self):

        self._client_socket = socket(AF_INET, SOCK_STREAM)

        self._connect()

    def _client_to_server_handler(self):

        # Welcome messages.
        print('\n=========HOW_TO===========')
        print("Enter {} to disconnect from the server.".format(CLIENT_QUIT_MESSAGE))
        print("Enter {} to get list of clients connected to server.".format(CLIENT_CLIENTS_MESSAGE))
        print("Enter {Username} with space before a message to send it privately.")
        print('==========================\n')

        # As long as socket is not dead, keep sending messages to server.
        while True:

            msg = input()
            self._client_socket.send(msg.encode())

            # User wish do close the connection.
            if msg == CLIENT_QUIT_MESSAGE:
                self._client_socket.close()
                return

    def _server_to_client_handler(self):

        # As long as socket is not dead, keep checking for messages from server.
        while True:
            try:
                msg_from_server = self._client_socket.recv(Server.BUFFER_SIZE).decode("utf-8")
                if msg_from_server:
                    print(msg_from_server)

                    if msg_from_server == Server.SERVER_WELCOME_MESSAGE or msg_from_server == Server.SERVER_NAME_TAKEN_MESSAGE:

                        name = input().encode()
                        self._client_socket.send(name)

                    elif START_CHATTING in msg_from_server:

                        # Communication will be possible only after client's initial identification.
                        Thread(target=self._client_to_server_handler, args=()).start()
            except:
                msg = DISCONNECT_MSG if self._client_socket.fileno() == -1 else CONNECTION_ERR
                print(msg)

                return

    def _connect(self):

        self._client_socket.connect(Server.ADDRESS)

        print("%%% You are connected to {}:{} %%%".format(Server.ADDRESS[0], Server.ADDRESS[1]), '\n')

        # Handle server communication.
        Thread(target=self._server_to_client_handler, args=()).start()


# =================MAIN===================== #

if __name__ == '__main__':
    client = Client()
