import socket

host = str(input("podaj adres IP serwera"))
port = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    sock.connect((host, port))
    received = sock.recv(1024)
    if str(received) == "Podaj X":
        move = int(input("podaj Y"))
        sock.sendall(move)
    if str(received) == "Podaj Y":
        move = int(input("podaj Y"))
        sock.sendall(move)
    if isinstance(received, int):
        for table_row_number in range(received):
            table_row = sock.recv(1024)
            print (table_row)
    if str(received) == "GRA": #ma sie zaczynac od tego, a nie byc tym! wyrazenie regularne needed
        print (received)
        break
print ("Zapraszam ponownie")