import sys
import random
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class XOGame:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = ["X", "O"]
        self.position = {}
        self.__prepare_map()

    def draw_map(self):
        for i in range(self.height):
            for n in range(self.width):
                sys.stdout.write(self.position[i, n])
            print("")

    def check_win(self):
        for i in range(self.height):
            for n in range(self.width):
                try:
                    if (self.position[i, n] == self.position[i, n + 1] == self.position[i, n + 2] in self.players or
                            self.position[i, n] == self.position[i + 1, n + 1] == self.position[
                                i + 2, n + 2] in self.players or
                            self.position[i, n] == self.position[i + 1, n - 1] == self.position[
                                i + 2, n - 2] in self.players or
                            self.position[i, n] == self.position[i + 1, n] == self.position[i + 2, n] in self.players):
                        print("Gratulacje! {} wygrali!".format(self.position[i, n]))
                        return "won"
                except:
                    pass

    def do_move(self, x, y, player):
        if self.position[y, x] == "-":
            self.position[y, x] = player
        else:
            print("zajete! tracisz ture gamoniu")

    def make_round(self):
        for player in self.players:
            if player == "Y":
                self.player_react_online(player)
            else:
                self.player_react_local(player)

    def is_map_full(self):
        for i in range(self.height):
            for j in range(self.width):
                try:
                    if self.position[i, j] == "-":
                        return "still_playing"
        return "remis"

    def player_react_local(self, player):
        try:
            x = int(input("Ruch {}. Podaj kolumne!".format(player)))
            y = int(input("Ruch {}. Podaj wiersz!".format(player)))
        except:
            print("nie wiem co chciales osiagnac, ale tracisz ture")
            self.do_move(x - 1, y - 1, player)

    def player_react_online(self, player):
        self.draw_map()
        try:
            conn.sendall("Ruch {}. Podaj kolumne!".format(player))
            x = int(conn.recv(1024))
            conn.sendall("Ruch {}. Podaj wiersz!".format(player))
            y = int(conn.recv(1024))
        except:
            print("nie wiem co chciales osiagnac, ale tracisz ture")
            self.do_move(x - 1, y - 1, player)

    def __prepare_map(self):
        for i in range(self.height):
            for n in range(self.width):
                self.position[i, n] = "-"


try:
    width = int(input("podaj szerokosc planszy(tak przynajmniej z 4): "))
    height = int(input("podaj wysokosc planszy(tak przynajmniej ze 4): "))
    if (width < 5) or (height < 4):
        raise DimensionError

except:
    width = random.randint(4, 8)
    height = random.randint(4, 8)
    print("nie kumasz to ja ci wybiore. szerokość to {}, a wysokosc {}".format(width, height))

game = XOGame(width, height)
result = "still_playing"

server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)
conn, addr = s.accept()

try:
    while result == "still_playing":
        game.make_round()
        result = game.check_win()
        result = game.is_map_full()
finally:
    conn.close()

if result == "remis":
    print("No niestety, remis.")
print("Koniec gry!")
