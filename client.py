import socket
from typing import Union

host = "127.0.0.1"  # str(input("podaj adres IP serwera"))
port = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flag = 0


def coder(data: Union[int, str, bytes]):
    if not isinstance(data, bytes):
        return bytes(str(data), "utf-8")
    if bytes == "":
        return 1
    if isinstance(data, bytes):
        data = str(data, "utf-8")
        if data.isdecimal():
            return int(data)
        else:
            return data


while True:
    if flag == 0:
        sock.connect((host, port))
        flag = 1
        print("polaczylem sie z {}".format(host))
    received = sock.recv(1024)
    if coder(received) == "Podaj X":
        move = int(input("podaj X"))
        sock.sendall(coder(move))
    if coder(received) == "Podaj Y":
        move = int(input("podaj Y"))
        sock.sendall(coder(move))
        flag = 0
    if isinstance(received, int):
        for table_row_number in range(received):
            table_row = sock.recv(1024)
            print(coder(table_row))
    if str(received) == "GRA":  # ma sie zaczynac od tego, a nie byc tym! wyrazenie regularne needed
        print(received)
        break
print("Zapraszam ponownie")
