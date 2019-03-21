import pickle
import socket
from enum import Enum

host = "127.0.0.1"
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flag = 0


class MessageType(Enum):
    BOARD_SEND = 0
    X_REQUEST = 1
    Y_REQUEST = 2
    X_RESPONSE = 3
    Y_RESPONSE = 4


sock.connect((host, port))


def __send_move_request(self, request_type: MessageType, response_type: MessageType):
    response = (None, None)

    while response[0] != response_type:
        sock.send(pickle.dumps((request_type, None)))
        response = pickle.loads(self.__connection.recv(1024))


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
