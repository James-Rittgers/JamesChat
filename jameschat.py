import socket

class Jameschat():

  def __init__(self):
    '''
    Initializes message reception and necessary variables
    '''
    self.ip_address = socket.gethostbyname(socket.gethostname())
    self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.recv_port = 5_000
    self.recv_socket.bind((self.ip_address, self.recv_port))
  
    self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


  def init_send(self, tgt_ip, tgt_port):
    '''
    Initializes message sending
    '''
    self.send_socket.connect((tgt_ip, tgt_port))

    raise NotImplementedError
    
  def decode_msg(self, msg):
    '''
    Decodes a message
    '''
    msg = msg.decode('UTF-8')
    msg = str(msg)
    msg = msg.split('|')

    return msg
 

  def send(self, cmd, msg=None):
    '''
    Sends msg to the tgt_port at tgt_address.
    '''
    self.send_socket.send(bytes(f'{self.ip_address}|{self.recv_port}|{cmd}|{msg}|',
                           'UTF-8'))
    
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


  class JameschatServer():

    def __init__(self):
      self.client_list = []


    def server_send(self, client_num, cmd, msg):
      '''
      Server sending, sends to client specified by IP and port
      '''
      sockety = client_list[client_num]
      sockety = sockety['sendto_socket']

      sockety.send(bytes(f'{self.ip_address}|{self.recv_port}|{cmd}|{msg}|',
                        'UTF-8'))


    def add_client(self, ip, port):
      '''
      Adds a client to the client list
      '''
      self.client_list.append({
        "client_IP": ip,
        "client_port": port,
        "sendto_socket": socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(ip, port)
      })

    
    def ping(self):
      '''
      Sends a PING command to all connected IPs
      '''
      for item in self.client_list:
        self.server_send(item['client_IP'], item['client_port'], 'PING')


  class JameschatClient():

    def __init__(self):
      raise NotImplementedError
    
    
    def connect_to_server(self, ip, port):
      '''
      Attempts to connect to the server at IP on port.
      Initializes sending and recieving capabilities.
      '''
      try:
        self.init_send(ip, port)

      except:
        raise ConnectionError
      
      try:
        self.recv_socket.bind((self.ip_address, self.main_recv_port))
      
      except:
        raise ConnectionError
      

    
    
    

