import pickle
import re
import socket
import time
from enum import Enum
from typing import Union, List, Tuple
possible_players = ["Y", "Z", "O", "X"]

class MessageType(Enum):
    BOARD_SEND = 0
    X_REQUEST = 1
    Y_REQUEST = 2
    X_RESPONSE = 3
    Y_RESPONSE = 4


# class Player:
#     def __init__(self, mark: str):
#         if len(mark) != 1:
#             # raise PlayerMarkError("Symbol gracza musi mieć jeden znak!")
#             pass
#         self.__mark = mark
#         self.__address = "127.0.0.1"  # str(input("Podaj adres IP gracza ".format(self.__mark)))
#
#     @property
#     def address(self):  # po drugie chwali sie swoim adresem
#         return self.__address
#
#     @property
#     def mark(self):  # po trzecie chwali sie swoim znakiem
#         return self.__mark


class NetPlayer:
    def __init__(self, connection: socket):
        # self.__port = 1234
        # self.__net_player = net_player
        # self.__sock = None
        # self.__connection = None
        self.__mark = possible_players.pop(-1)
        self.__connection = connection

    # def connect_to_player(self):
    #     self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.__sock.bind((self.__net_player.address, self.__port))
    #     self.__sock.listen(1)
    #     self.__connection, address = self.__sock.accept()
    #     print("polaczylem sie! typek to{}".format(address))

    def send_board(self, string_board: str):
        self.__connection.send(string_board)

    def get_move_coordinates(self) -> Tuple[int, int]:
        x = self.__send_move_request(MessageType.X_REQUEST, MessageType.X_RESPONSE)
        y = self.__send_move_request(MessageType.Y_REQUEST, MessageType.Y_RESPONSE)
        return x, y

    def end_connection(self):  # konczy polaczenie
        self.__connection.close()

    def tell_who_won(self, mark: str):
        self.__connection.sendall("GRA SKONCZONA. {} WYGRAL!".format(mark))

    def __send_move_request(self, request_type: MessageType, response_type: MessageType) -> int:
        response = (None, None)

        while response[0] != response_type:
            time.sleep(0.2)
            self.__connection.send(pickle.dumps((request_type, None)))
            response = pickle.loads(self.__connection.recv(1024))

        return response[1]


    @property
    def mark(self):
        return self.__mark


class Server:
    def __init__(self):
        self.__socket = self.__create_socket("127.0.0.1", 12345)

    def wait_for_players(self, number_of_players: int) -> List[NetPlayer]:
        return [NetPlayer(self.__socket.accept()[0]) for _ in range(number_of_players)]

        # self.__socket.sendall(board.encode())
        # self.__connection_table.append(connection)
        # print("jest! mamy gnoja! a imie jego: {}".format(address))

    def close_socket(self):
        self.__socket.close()

    @staticmethod
    def __create_socket(hostname: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((hostname, port))
        sock.listen(2)
        return sock


# class MessagePacker:
#     @staticmethod
#     def pack_message(message_type: MessageType, data: Any) -> Tuple[int, str]:
# return


class Board:  # ta klasa nie zmienila sie za wiele
    def __init__(self, board_height: int, board_width: int):
        self.__width = board_width
        self.__height = board_height
        self.__board = [["-" for _ in range(board_width)] for _ in range(board_height)]

    def check_win(self) -> Union[str, bool]:
        checked_wins = [self.__check_all_win_vectors(0, 1),
                        self.__check_all_win_vectors(1, 0),
                        self.__check_all_win_vectors(1, 1),
                        self.__check_all_win_vectors(1, -1)]
        for checked_win in checked_wins:
            if checked_win:
                return checked_win

    def __check_all_win_vectors(self, delta_x: int, delta_y: int) -> Union[str, bool]:
        for y, board_row in enumerate(self.__board):
            for x in range(len(board_row)):
                single_win_vector = self.__check_single_win_vector(x, y, delta_x, delta_y)
                if single_win_vector:
                    return single_win_vector
        return False

    def __check_single_win_vector(self, current_x: int, current_y: int, delta_x: int, delta_y: int) -> Union[str, bool]:
        row_string = ""
        while self.__are_coordinates_in_board_range(current_x, current_y):
            row_string += self.__board[current_x][current_y]
            current_x += delta_x
            current_y += delta_y
        found_result = re.search(r"([^\-])\1\1", row_string)
        if found_result:
            return found_result.groups()[0]
        else:
            return False

    def is_board_full(self) -> bool:
        for board_row in self.__board:
            for cell in board_row:
                if cell == "-":
                    return False
        return True

    def __are_coordinates_in_board_range(self, x: int, y: int) -> bool:
        return (x < self.__width) and (y < self.__height)

    def put_mark_if_possible(self, mark: str, x: int, y: int) -> bool:
        if self.__are_coordinates_in_board_range(x,y):
            if (self.__board[x][y] == "-"):
                self.__board[x][y] = mark
                return True
        return False

    def show_board(self) -> str:
        string_board = "\n".join([" ".join(row) for row in self.__board])
        return string_board


class XOGame:
    def __init__(self, play_board: Board, connection_table: List[NetPlayer]):
        # TODO: zrobic zeby NetPlayer i np. jakis ComputerPLayer mialy interfejs (i stworzyc ComputerPLayer)
        self.__board = play_board
        self.__player_list = connection_table
        # self.__server = server

    def play_round(self):  # funkcja robi standardowy zestaw czynnosci potrzebny do rozgerania tury
        for player in self.__player_list:
            self.__send_board_to_all(self.__board.show_board())
            x, y = player.get_move_coordinates()
            self.__board.put_mark_if_possible(player.mark, x, y)
        return self.__board.check_win()

        # for actual_player in self.__connection_table:
        #     actual_player.send_board(self.__board.show_board())
        #     x, y = actual_player.do_move()
        #     print(x)
        #     print(y)
        #     self.__board.put_mark_if_possible(actual_player.mark, x, y)
        #     actual_player.end_connection()
        # return self.__board.check_win()

    def tell_who_won(self, mark: str):
        for actual_player in self.__player_list:
            actual_player.tell_who_won(mark)
            actual_player.end_connection()

    def is_board_full(self) -> bool:
        return self.__board.is_board_full()

    def __send_board_to_all(self, string_board: str):
        for connection in self.__player_list:
            connection.send_board(pickle.dumps((MessageType.BOARD_SEND, string_board)))


if __name__ == '__main__':  # gra nie ruszy jeżeli nie jest mainem
    width = 5  # int(input("Podaj szerokosc"))
    height = 5  # int(input("podaj wysokosc"))
    board = Board(width, height)
    # player_list = [Player("X"), Player("O")]  # tutaj można dopisać nowych graczy
    server = Server()
    player_list = server.wait_for_players(2)
    # connection_table = [NetPlay(player) for player in player_list]
    #try:
    game = XOGame(board, player_list)
    while True:
        result = game.play_round()
        if result:
            break
    #except Exception:
    #    server.close_socket()
    #finally:
    #    server.close_socket()

    #
    # while not game.is_board_full():
    #     winning_symbol = game.play_round()
    #     if winning_symbol:
    #         game.tell_who_won(winning_symbol)  # jeżeli ktos wygra to obaj gracze dostana o tym infromacje
    #         break
    # if game.is_board_full():
    #     game.tell_who_won("NIKT NIE")  # analogicznie jezeli nikt nie wygra
print("Gra zakonczona.")
