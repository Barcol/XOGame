import re
import socket
from typing import Union, List


class Player:  # zadania tej klasy zostaly mocno obciete. W zasadzie to pozostaly tylko 3.
    def __init__(self, mark: str):  # po pierwsze sprawdza czy ma jeden znak
        if len(mark) != 1:
            # raise PlayerMarkError("Symbol gracza musi mieć jeden znak!")
            pass
        self.__mark = mark
        self.__adress = str(input("Podaj adres IP gracza ".format(self.__mark)))

    @property
    def get_adress(self):  # po drugie chwali sie swoim adresem
        return self.__adress

    @property
    def get_mark(self):  # po trzecie chwali sie swoim znakiem
        return self.__mark


class NetPlay:
    def __init__(self, player: Player):  # konstruktor jedynie przypisuje adres klienta
        self.__adress = player.get_adress  # na kazdego gracza przypada jeden obiekt tej klasy
        self.__port = 1234  # port jest jeden dla kazdego

    def connect_to_player(self):  # natomiast za laczenie odpowiada ta funckja (wywolujemy przed kazdym rchem gracza!)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((self.__adress, self.__port))
        self.__sock.listen(1)
        self.__conn, self.__addr = self.__sock.accept()
        print("polaczylem sie! typek to".format(self.__addr))
        print("test")

    def draw_map(self, ready_board):
        self.__conn.sendall(self.coder(len(ready_board)))  # wysylamy klientowi wysoksc tabeli
        for row in ready_board:  # dla każdego wiersza w tabeli
            self.__conn.sendall(self.coder(" ".join(row)))

    def do_move(self):  # po wyswietleniu klientowi obecnego stanu rzeczy, pytamy go o wspolrzedne
        self.__conn.sendall(self.coder("Podaj X"))
        x = self.__conn.recv(1024)
        self.__conn.sendall(self.coder("Podaj Y"))
        y = self.__conn.recv(1024)
        return x, y  # funkcja zwraca co zdecydowal gracz. rola obiektu zostala zakonczona

    def end_connection(self):  # konczy polaczenie
        self.__conn.close()

    def tell_who_won(self, mark: str):
        self.__conn.sendall(self.coder("GRA SKONCZONA. {} WYGRAL!".format(mark)))

    def coder(self, data: Union[int, str, bytes]):
        if not isinstance(data, bytes):
            return bytes(data, "utf-8")
        if bytes == "":
            return 1
        if isinstance(data, bytes):
            data = str(data, "utf-8")
            if data.isdecimal():
                return int(data)
            else:
                return data

    @property
    def get_mark(self):
        return player.get_mark


class Board:  # ta klasa nie zmienila sie za wiele
    def __init__(self, height: int, width: int):
        self.__height = height
        self.__width = width
        self.__board = [["-" for _ in range(self.__width)] for _ in range(self.__height)]

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
            row_string += self.__board[current_y][current_x]
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
        if (x <= self.__width) and (y <= self.__height):
            return True
        return False

    def put_mark_if_possible(self, mark: str, x: int, y: int) -> bool:
        if self.__are_coordinates_in_board_range and (self.__board[x][y] == "-"):
            self.__board[x][y] = mark
            return True
        return False

    def show_board(self):
        return self.__board


class XOGame:
    def __init__(self, board: Board, connection_table: List[NetPlay]):
        self.__board = board
        self.__connection_table = connection_table

    def play_round(self) -> Union[str, bool]:  # funkcja robi standardowy zestaw czynnosci potrzebny do rozgerania tury
        for player in self.__connection_table:
            player.connect_to_player()
            player.draw_map(self.__board.show_board())
            x, y = player.do_move()
            print(x)
            print(y)
            self.__board.put_mark_if_possible(player.get_mark, int(x, base=2), int(y, base=2))
            player.end_connection()
            return board.check_win()

    def tell_who_won(self, mark: str):
        for player in self.__connection_table:
            player.connect_to_player()
            player.tell_who_won(mark)
            player.end_connection()

    def is_board_full(self) -> bool:
        return board.is_board_full()


if __name__ == '__main__':  # gra nie ruszy jeżeli nie jest mainem
    connection_table = []
    width = 5  # int(input("Podaj szerokosc"))
    height = 4  # int(input("podaj wysokosc"))
    board = Board(width, height)
    player_list = [Player("X"), Player("O")]  # tutaj można dopisać nowych graczy
    for player in player_list:  # i dla każdego z nich
        connection_table.append(NetPlay(player))  # tworzony jest nowy obiekt do obslugi socketa
    game = XOGame(board, connection_table)  # to do gry wchodza juz same one, a nie player_list

    while not game.is_board_full():
        winning_symbol = game.play_round()
        if winning_symbol:
            game.tell_who_won(winning_symbol)  # jeżeli ktos wygra to obaj gracze dostana o tym infromacje
            break
    if game.is_board_full():
        game.tell_who_won("NIKT NIE")  # analogicznie jezeli nikt nie wygra
print("Gra zakonczona.")
