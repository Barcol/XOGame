import pickle
import socket
from enum import Enum
from typing import Union

host = "127.0.0.1"  # str(input("podaj adres IP serwera"))
port = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flag = 0

class MessageType(Enum):
    BOARD_SEND = 0
    X_REQUEST = 1
    Y_REQUEST = 2
    X_RESPONSE = 3
    Y_RESPONSE = 4


# def coder(data: Union[int, str, bytes]):
#     if not isinstance(data, bytes):
#         return bytes(str(data), "utf-8")
#     if bytes == "":
#         return 1
#     if isinstance(data, bytes):
#         data = str(data, "utf-8")
#         if data.isdecimal():
#             return int(data)
#         else:
#             return data


sock.connect((host, port))


def __send_move_request(self, request_type: MessageType, response_type: MessageType) -> int:
    response = (None, None)

    while response[0] != response_type:
        sock.send(pickle.dumps((request_type, None)))
        response = pickle.loads(self.__connection.recv(1024))



try:
    while 1:
        x = sock.recv(1024)
        if x:
            a = pickle.loads(x)
            if a[0] == MessageType.X_REQUEST:
                move = int(input("podaj X"))
                sock.send(pickle.dumps((MessageType.X_RESPONSE, move)))
            elif a[0] == MessageType.Y_REQUEST:
                move = int(input("podaj Y"))
                sock.send(pickle.dumps((MessageType.Y_RESPONSE, move)))
            elif a[0] == MessageType.BOARD_SEND:
                print(a[1])
except KeyboardInterrupt:
    sock.close()
# while True:
#     # if flag == 0:
#     #     flag = 1
#     #     print("polaczylem sie z {}".format(host))
#     received = sock.recv(1024)
#     if coder(received) == "Podaj X":
#         move = int(input("podaj X"))
#         sock.sendall(coder(move))
#     if coder(received) == "Podaj Y":
#         move = int(input("podaj Y"))
#         sock.sendall(coder(move))
#         flag = 0
#     if isinstance(received, int):
#         for table_row_number in range(received):
#             table_row = sock.recv(1024)
#             print(coder(table_row))
#     if str(received) == "GRA":  # ma sie zaczynac od tego, a nie byc tym! wyrazenie regularne needed
#         print(received)
#         break
# print("Zapraszam ponownie")
