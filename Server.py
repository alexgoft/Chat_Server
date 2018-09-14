# ================IMPORTS======================#
import select
import socket

# ================CONSTANTS======================#

WELCOME_MESSAGE = "Welcome!! Please enter your nickname:"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 80
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)


# =================CLASS=====================#

class Server:

    def __init__(self):

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(ADDRESS)
        self._server_socket.listen(5)

        self._clients = {}

        self._socket_list = []
        self._socket_list.append(self._server_socket)

        self._run()

    def _run(self):
        print('%%% Server is up and running %%%')
        print('%%% Server Address {}:{} %%%'.format(HOST, PORT), '\n')

        while True:
            ready_to_read, ready_to_write, in_error = select.select(self._socket_list, [], [], 0)
            for sock in ready_to_read:
                if sock == self._server_socket:

                    client_socket, client_address = self._server_socket.accept()
                    self._clients.setdefault(client_socket, {})['client_address'] = client_address

                    if 'client_name' not in self._clients[client_socket]:
                        # First message exchange - Get name of client and start communication.
                        client_socket.send(WELCOME_MESSAGE.encode())
                        client_name = client_socket.recv(BUFFER_SIZE).decode("utf-8")

                        self._clients[client_socket]['client_name'] = client_name
                        self._socket_list.append(client_socket)

                        print("{} has connected.".format(client_name))
                else:
                    client_msg = sock.recv(BUFFER_SIZE).decode("utf-8")
                    curr_client_msg = "{}: {}".format(self._clients[sock]['client_name'], client_msg)
                    print(curr_client_msg)

                    # Broadcast msg to all connections ("Public Forum").
                    for s in self._socket_list:
                        if s != self._server_socket and s != sock:
                            s.send(curr_client_msg.encode())


if __name__ == '__main__':
    server = Server()
