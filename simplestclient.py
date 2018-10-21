import socket

host = "localhost"
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

while True:
    data = input("wpisz cos")
    sock.sendall(bytes(data, "utf-8"))
    received = sock.recv(1024)
    print(received)
