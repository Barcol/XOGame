import random
import socket
from typing import Union

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class XOGame:  # usunalem nowa linie przed initem
    __players = ["x", "o"] # zmienilem players na prywatna statyczna zmienną (bo kazda gra bedzie miala tych graczy)

    def __init__(self, width: int, height: int): # dodalem type hinty do argumentow
        self.__next_player = self.__players[0]
        print(self.__next_player)
        # usunalem self.width i self.height bo nie sa potrzebne (w innych metodach bedziemy iterowac po self.__board)
        self.__board = [["-" for _ in range(width)] for _ in range(height)]  # zmienilem zmienna obiektu self.position na self.__board
        # usunalem metode self.__prepare_map (bo zostala zastapiona powyzsza linijka)

    def draw_map(self):
        for board_row in self.__board:
            board_row_str = " ".join(board_row)  # to laczy elementy listy za pomoca stringa od ktorego sie ta metode wywola (tutaj " ")
            print(board_row_str)  # uzywaj printa zamiast sys.stdout.write

    def check_win(self) -> Union[str, bool]: # przerobilem ta metode zeby uzywala prywatnej metody ktora sprawdza w inny sposob
        checked_wins = [self.__check_win_with_deltas(1, 0),
                        self.__check_win_with_deltas(0, 1),
                        self.__check_win_with_deltas(1, 1),
                        self.__check_win_with_deltas(1, -1)]

        for checked_win in checked_wins:
            if checked_win is not False:
                return checked_win

        return False

    def do_move(self, x: int, y: int):  # dodalem type hinty do argumentow i usunalem argument "player" (bo teraz sama klasa wie kto bedzie mial nastepny ruch)
        if self.__board[y][x] == "-":
            self.__board[y][x] = self.__next_player

            next_player_index = (self.__players.index(self.__next_player) + 1) % len(self.__players)
            self.__next_player = self.__players[next_player_index]
        else:
            print("zajete! tracisz ture gamoniu")

    def is_board_full(self) -> bool: # dodalem type hint ze zwraca cos typu bool
        # zmienilem ta metode zeby zwracala true albo false (bo stringami sie trudno operuje pozniej)
        for single_row in self.__board:
            for symbol in single_row:
                if symbol == "-":
                    return False
        return True

    # def make_round(self):
    #     for player in self.players:
    #         if player == "Y":
    #             self.player_react_online(player)
    #         else:
    #             self.player_react_local(player)
    #

    #
    # def player_react_local(self, player):
    #     try:
    #         x = int(input("Ruch {}. Podaj kolumne!".format(player)))
    #         y = int(input("Ruch {}. Podaj wiersz!".format(player)))
    #     except:
    #         print("nie wiem co chciales osiagnac, ale tracisz ture")
    #         self.do_move(x - 1, y - 1, player)
    #
    # def player_react_online(self, player):
    #     self.draw_map()
    #     try:
    #         conn.sendall("Ruch {}. Podaj kolumne!".format(player))
    #         x = int(conn.recv(1024))
    #         conn.sendall("Ruch {}. Podaj wiersz!".format(player))
    #         y = int(conn.recv(1024))
    #     except:
    #         print("nie wiem co chciales osiagnac, ale tracisz ture")
    #         self.do_move(x - 1, y - 1, player)

    def __check_win_with_deltas(self, delta_x: int, delta_y: int) -> Union[str, bool]:  # union znaczy ze moze to byc string albo bool
        for y, board_row in enumerate(self.__board):
            for x in range(len(board_row)):
                symbol_string = ""
                temp_x = x
                temp_y = y

                while (0 <= temp_x < len(board_row)) and (0 <= temp_y < len(self.__board)):
                    symbol_string += self.__board[temp_y][temp_x]
                    temp_x += delta_x
                    temp_y += delta_y

                for player in self.__players:
                    if player * 3 in symbol_string:
                        return player
        return False


if __name__ == '__main__':  # dodalem ta linie. Warto ją dawac, bo gdy zaimportujesz ten plik to dzieki tej linii kod ponizej ci sie nie wykona (no chyba ze rzeczywiscie chcesz zeby przy imporcie tego pliku ten kod sie wykonywal)
    width = int(input("podaj szerokosc planszy(tak przynajmniej z 4): "))
    height = int(input("podaj wysokosc planszy(tak przynajmniej ze 4): "))

    # jesli nie jest to konieczne to unikaj try exceptow i zastap je ifem albo czyms innym, tak jak ja tu zrobilem
    if (width < 5) or (height < 4):
        width = random.randint(4, 8)
        height = random.randint(4, 8)
        print("nie kumasz to ja ci wybiore. szerokość to {}, a wysokosc {}".format(width, height))

    game = XOGame(width, height)

    while not game.is_board_full():
        game.draw_map()

        x = int(input("podaj x"))
        y = int(input("podaj y"))

        game.do_move(x, y)
        winning_player = game.check_win()

        if winning_player:
            print("wygraly {}".format(winning_player))
            break

    print("gra skonczona")

    # result = "still_playing"
    #
    # server_address = ('localhost', 10000)
    # print('starting up on {} port {}'.format(*server_address))
    # sock.bind(server_address)
    # sock.listen(1)
    # conn, addr = sock.accept()
    #
    # try:
    #     while result == "still_playing":
    #         game.make_round()
    #         result = game.check_win()
    #         result = game.is_map_full()
    # finally:
    #     conn.close()
    #
    # if result == "remis":
    #     print("No niestety, remis.")
    # print("Koniec gry!")
