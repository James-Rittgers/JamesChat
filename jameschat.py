import socket
import sys
from random import randint
from time import sleep


class Jameschat:

    def __init__(self):
        """
        Initializes message reception and necessary variables
        """
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_port = randint(1000, 1050)
        self.recv_socket.bind((self.ip_address, self.recv_port))



        self.username = None
        self.chatlog = ''

    def set_username(self, username):
        """
        Sets the username
        """

        self.username = username

    def decode_msg(self, msg):
        """
        Decodes a message
        """
        msg = msg.decode("UTF-8")
        msg = str(msg)
        msg = msg.split("|")

        return_dict = {
            "sender_ip": msg[0],
            "sender_recv_port": msg[1],
            "cmd": msg[2],
            "msg": msg[3],
        }

        return return_dict

    def listen_for_cmd(self, tgt_cmd):
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
                print("Something recieved")
                msg = self.decode_msg(recv_buffer)

                if msg["cmd"] == tgt_cmd:
                    return msg

                else:
                    self.listen_for_cmd(tgt_cmd)

        except TimeoutError:
            print("Timeout")
            #sys.exit()

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
        self.client_dict = {}
        self.usernames = {self.ip_address: self.username}

    def set_username(self, username):
        """
        Sets the username
        """

        self.username = username
        self.usernames[self.ip_address] = username
        print(f'{self.username} has joined the chat')

    def send_to_all(self, cmd, msg=None):
        """
        Sends a message to all connected hosts
        """

        for host in self.client_dict:
            self.server_send(host[1], cmd, msg)

    def add_msg_to_chatlog(self, msg):
        """
        Adds a new message to the chatlog, then sends out to all connected hosts
        """

        self.chatlog += f'\n{msg}'
        self.send_to_all(cmd='CHT-ENTRY', msg=msg)

    def server_send(self, ip, cmd, msg=None):
        """
        Server sending, sends to client specified by IP and port
        """
        sockety = self.client_dict[ip]

        sockety.send(bytes(f"{self.ip_address}|{self.recv_port}|{cmd}|{msg}", "UTF-8"))

    def add_client(self, ip, port, username):
        """
        Adds a client to the client list
        """
        sockety = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockety.connect((ip, int(port)))

        self.client_dict.update({ip: sockety})
        self.usernames.update({ip: username})

    def allow_connection(self):
        """
        Allows connection.
        Exits when one device is connected.
        """

        msg = self.listen_for_cmd("CLIENT-CONN")
        self.add_client(msg["sender_ip"], msg["sender_recv_port"], msg["msg"])

        self.server_send(msg["sender_ip"], "CONN-OK")
        print(f'{msg[msg]} has joined the chat')

    def run_networking(self):

        while True:
            inbound = self.listen()
            command = inbound["cmd"]
            message = inbound["msg"]


            if command == "NW-MSG":
                self.add_msg_to_chatlog(message)
                print(message)

            elif command == "CLIENT-CONN":
                self.add_client(inbound["sender_ip"], inbound["sender_recv_port"], message)
                self.server_send(inbound["sender_ip"], "CONN-OK")
                print(f'\n{message} has joined the chat')

            sleep(0.5)

            


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

        self.send(cmd="CLIENT-CONN", msg=self.username)

        self.listen_for_cmd("CONN-OK")

        return True
    
    def run_networking(self):

        while True:
            inbound = self.listen()
            command = inbound["cmd"]
            message = inbound["msg"]


            if command == "CHT-ENTRY":
                self.chatlog += message
                print(message)