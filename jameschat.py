import socket

class Jameschat():

  def __init__(self):
    '''
    Initializes message reception and necessary variables
    '''
    self.ip_address = socket.gethostbyname(socket.gethostname())
    self.main_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.main_recv_port = 5_000
    self.main_recv_socket.bind((self.ip_address, self.recv_port))

    self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  def init_send(self, tgt_ip):
    '''
    Initializes message sending
    '''
    self.send_socket.connect(tgt_ip)
    raise NotImplementedError

  def decode_msg(self, msg):
    '''
    Decodes a message
    '''
    raise NotImplementedError

  def send(self, tgt_address, tgt_port, cmd, msg=None):
    '''
    Sends msg to the tgt_port at tgt_address.
    msg must be a JameschatMessage.
    '''
    raise NotImplementedError
  
  
  def listen_for_cmd(self, cmd):
    '''
    Listens for the specific command specified by cmd.
    Will run until timeout or it recieves the message.
    '''
    raise NotImplementedError
  
  def listen(self):
    '''
    Listens for any messages. 
    Will run until timeout or it recieves any message, and will return the message.
    '''
    raise NotImplementedError


  class JameschatServer(self):

    def __init__(self):
      self.client_list = []

    def add_client(self):
      '''
      Adds a client to the client list
      '''
      raise NotImplementedError
    
    def ping(self):
      '''
      Sends a ping message to all connected IPs
      '''
      raise NotImplementedError


  class JameschatClient(self):

    def __init__(self):
      raise NotImplementedError
    
    
    def init_send(server_ip, server_port):
      '''
      Initializes sending capabilities to the server
      '''
  

    def connect_to_server(self):
      raise NotImplementedError
    
    
    

