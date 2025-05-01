import socket
import sys
from random import randint


class Jameschat:

    def __init__(self):
        """
        Initializes message reception and necessary variables
        """
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_port = randint(1000, 1050)
        self.recv_socket.bind((self.ip_address, self.recv_port))

    def decode_msg(self, msg):
        """
        Decodes a message
        """
        msg = msg.decode("UTF-8")
        msg = str(msg)
        msg = msg.split("|")

        return msg

    def listen_for_cmd(self, cmd):
        """
        Listens for the specific command specified by cmd.
        Will run until timeout or it recieves the message.
        Returns the message.
        """
        self.recv_socket.listen(5)

        try:
            connection, address = self.recv_socket.accept()
            recv_buffer = connection.recv(64)

            if len(recv_buffer) > 0:
                print('Something recieved')
                msg = self.decode_msg(recv_buffer)

                if msg[2] == cmd:
                    return msg

        except TimeoutError:
            print("Timeout")
            sys.exit()

    def listen(self):
        """
        Listens for any messages.
        Will run until timeout or it recieves any message, and will return the message.
        """
        self.recv_socket.listen(5)

        try:
            connection, address = self.recv_socket.accept()
            recv_buffer = connection.recv(64)

            if len(recv_buffer) > 0:
                msg = self.decode_msg(recv_buffer)
                return msg

        except TimeoutError:
            print("Timeout")
            sys.exit()


class JameschatServer(Jameschat):

    def __init__(self):
        super().__init__()
        self.client_list = []
        self.client_dict = {}

    def server_send(self, ip, cmd, msg=None):
        """
        Server sending, sends to client specified by IP and port
        """
        sockety = self.client_dict[ip]

        sockety.send(bytes(f"{self.ip_address}|{self.recv_port}|{cmd}|{msg}", "UTF-8"))

    def add_client(self, ip, port):
        """
        Adds a client to the client list
        """
        sockety = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockety.connect((ip, int(port)))

        self.client_list.append(
            {"client_IP": ip, "client_port": port, "sendto_socket": sockety}
        )

        self.client_dict.update({ip: sockety})

    def allow_connection(self):
        """
        Allows connection.
        Exits when one device is connected.
        """

        msg = self.listen_for_cmd("CLIENT-CONN")
        self.add_client(msg[0], msg[1])

        self.server_send(msg[0], "CONN-OK")


class JameschatClient(Jameschat):

    def __init__(self):

        super().__init__()
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, cmd, msg=None):
        """
        Sends msg to the tgt_port at tgt_address.
        """
        self.send_socket.send(
            bytes(f"{self.ip_address}|{self.recv_port}|{cmd}|{msg}|", "UTF-8")
        )

    def init_send(self, tgt_ip, tgt_port):
        """
        Initializes message sending
        """
        self.send_socket.connect((tgt_ip, tgt_port))

    def connect_to_server(self, ip, port):
        """
        Attempts to connect to the server at IP on port.
        Initializes sending and recieving capabilities.
        Returns True if connection successful.
        """

        self.init_send(ip, port)

        self.send(cmd="CLIENT-CONN")

        self.listen_for_cmd("CONN-OK")

        return True

    def ping(self):
        """
        Listens for ping then responds to server.
        """
        self.listen_for_cmd("PING")
