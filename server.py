import server_connect as sv
from inputimeout import inputimeout

# Init and konfigurasi Server
server = sv.setting_server()
alamat_server = ''
port_server = 5050

server.start_server(alamat_server, port_server)

# Connect Client1
client_1 = server.connect_to_client()

# Connect Client2
client_2 = server.connect_to_client()

time_over = ''
while time_over != "break":
  try:
      msg = inputimeout(prompt='Your Input Command:', timeout=3)
      if msg != "break":
        client_1.send(str.encode(msg))
        client_2.send(str.encode(msg))

  except Exception:
      dataclient1 = server.get_data_client(client_1)
      if dataclient1 != "Time Out":
         client_2.send(str.encode(dataclient1))
      
      dataclient2 = server.get_data_client(client_2)
      if dataclient2 != "Time Out":
         client_1.send(str.encode(dataclient2))
  
# Print the statement on timeoutprint(time_over)