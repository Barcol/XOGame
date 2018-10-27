#just an average echo server

import socket

adress = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((adress, port))

s.listen(1)
conn, addr = s.accept()

print("jest! mamy gnoja! a imie jego: {}".format(addr))

while True:
    data = conn.recv(1024)
    conn.sendall(data)
