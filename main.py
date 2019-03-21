import pickle
import re
import socket
from enum import Enum
from typing import Union, List, Tuple
possible_players = ["Y", "Z", "O", "X"]


class MessageType(Enum):
    BOARD_SEND = 0
    X_REQUEST = 1
    Y_REQUEST = 2
    X_RESPONSE = 3
    Y_RESPONSE = 4


class NetPlayer:
    def __init__(self, connection: socket):

        self.__mark = possible_players.pop(-1)
        self.__connection = connection

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
            print("Wysyłanie. Kod wiadomosci to {}".format(request_type))
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

    def close_socket(self):
        self.__socket.close()

    @staticmethod
    def __create_socket(hostname: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((hostname, port))
        sock.listen(2)
        return sock


class Board:
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
        if self.__are_coordinates_in_board_range(x, y):
            if self.__board[x][y] == "-":
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

    def play_round(self):
        for player in self.__player_list:
            self.__send_board_to_all(self.__board.show_board())
            x, y = player.get_move_coordinates()
            self.__board.put_mark_if_possible(player.mark, x, y)
        return self.__board.check_win()

    def tell_who_won(self, mark: str):
        for actual_player in self.__player_list:
            actual_player.tell_who_won(mark)
            actual_player.end_connection()

    def is_board_full(self) -> bool:
        return self.__board.is_board_full()

    def __send_board_to_all(self, string_board: str):
        for connection in self.__player_list:
            connection.send_board(pickle.dumps((MessageType.BOARD_SEND, string_board)))


if __name__ == '__main__':
    width = 5
    height = 5
    board = Board(width, height)
    server = Server()
    player_list = server.wait_for_players(2)
    game = XOGame(board, player_list)
    while True:
        result = game.play_round()
        if result:
            break
print("Gra zakonczona.")
