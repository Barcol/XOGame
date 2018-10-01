import random
import re
import socket
from typing import Union, Tuple, List


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




class Board:
    def __init__(self, width: int, height: int):
        self.__board = [["-" for _ in range(width)] for _ in range(height)]

    def draw_board(self):
        for board_row in self.__board:
            board_row_str = " ".join(board_row)
            print(board_row_str)

    def check_win(self) -> Union[str, bool]:
        checked_wins = [self.__check_all_win_vectors(1, 0),
                        self.__check_all_win_vectors(0, 1),
                        self.__check_all_win_vectors(1, 1),
                        self.__check_all_win_vectors(1, -1)]

        for checked_win in checked_wins:
            if checked_win is not False:
                return checked_win

    def is_board_full(self) -> bool:
        for single_row in self.__board:
            for symbol in single_row:
                if symbol == "-":
                    return False
        return True

    def put_mark_if_possible(self, x: int, y: int, player_mark: str) -> bool:
        if self.__are_coordinates_in_board_range(x, y) and self.__board[y][x] == "-":
            self.__board[y][x] = player_mark
            return True
        return False

    def __are_coordinates_in_board_range(self, x: int, y: int) -> bool:
        board_width = len(self.__board[0])
        board_height = len(self.__board)
        return (0 <= x < board_width) and (0 <= y < board_height)

    def __check_all_win_vectors(self, delta_x: int, delta_y: int) -> Union[str, bool]:
        for y, board_row in enumerate(self.__board):
            for x in range(len(board_row)):
                single_win_vector = self.__check_single_win_vector(x, y, delta_x, delta_y)

                if single_win_vector:
                    return single_win_vector
        return False

    def __check_single_win_vector(self, start_x: int, start_y: int, delta_x: int, delta_y: int) -> Union[str, bool]:
        symbol_string = ""

        while self.__are_coordinates_in_board_range(start_x, start_y):
            symbol_string += self.__board[start_y][start_x]
            start_x += delta_x
            start_y += delta_y

        found_result = re.search(r"([^\-])\1\1", symbol_string)

        if found_result:
            return found_result.groups()[0]
        else:
            return False







class Player:
    def __init__(self, mark: str):
        if len(mark) != 1:
            raise ValueError("mark must be single character string")

        self.__mark = mark
        self.__next_player = None

    @property
    def next_player(self) -> "Player":
        return self.__next_player

    @next_player.setter
    def next_player(self, next_player: "Player"):
        if self.__next_player is None:
            self.__next_player = next_player

    def do_move(self, board: Board) -> bool:
        x = int(input("podaj x"))
        y = int(input("podaj y"))

        return board.put_mark_if_possible(x, y, self.__mark)










class XOGame:
    def __init__(self, player_list: List[Player], board: Board):
        for player, next_player in zip(player_list, player_list[1:] + [player_list[0]]):
            player.next_player = next_player

        self.__actual_player = player_list[0]
        self.__board = board

    def do_move(self):
        if not self.__actual_player.do_move(self.__board):
            print("zajete! tracisz ture gamoniu")

        self.__actual_player = self.__actual_player.next_player

    def draw_board(self):
        self.__board.draw_board()

    def check_win(self) -> Union[str, bool]:
        return self.__board.check_win()

    def is_board_full(self) -> bool:
        return self.__board.is_board_full()








if __name__ == '__main__':
    width = int(input("podaj szerokosc planszy(tak przynajmniej z 4): "))
    height = int(input("podaj wysokosc planszy(tak przynajmniej ze 4): "))


    if (width < 5) or (height < 4):
        width = random.randint(4, 8)
        height = random.randint(4, 8)
        print("nie kumasz to ja ci wybiore. szerokość to {}, a wysokosc {}".format(width, height))

    board = Board(width, height)
    player_list = [Player("X"), Player("O")]
    game = XOGame(player_list, board)

    while not game.is_board_full():
        game.draw_board()
        game.do_move()
        winning_symbol = game.check_win()

        if winning_symbol:
            print("wygraly {}".format(winning_symbol))
            break

    print("gra skonczona")
