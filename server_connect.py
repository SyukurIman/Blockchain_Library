import socket
from _thread import *

class setting_server:
  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.ThreadCount = 0

  def start_server(self, ip, port):
    try:
      self.socket.bind((ip, port))
    except socket.error as e:
      print(str(e))
    self.socket.listen(10)
    print ("socket is listening") 

  def connect_to_client(self):
    Client, addr = self.socket.accept()
    print("client telah terhubung ", addr)
    return Client
  
  def control_robot(self, client1, client2):
    while True:
      data_input = input("Your Input General: ")
      if data_input == "exit":
        break
      if data_input == 'start':
        client1.send(str.encode(input))
        client2.send(str.encode(input))
      elif data_input == '':
        data_client1 = self.get_data_client(client1)
        data_client2 = self.get_data_client(client2)

        if data_client1 != 'Time Out':
          print(data_client1)
        if data_client2 != 'Time Out':
          print(data_client2)
  
  def get_data_client(self, client):
    self.socket.settimeout(1.0)
    try:
      Response = client.recv(2048).decode('utf-8')
    except socket.error as e:
      return "Time Out"
    return Response
  