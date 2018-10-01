import random
import sys

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
                        return False
                except:
                    pass
        return True

    def do_move(self, x, y, player):
        if self.position[y, x] == "-":
            self.position[y, x] = player
        else:
            print("zajete! tracisz ture gamoniu")

    def make_round(self):
        for player in self.players:
           self.player_react(player)

    def is_map_full(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.position[i, j] == "-":
                    return "still_playing"
        return "remis"

    def player_react(self, player):
        try:
            x = int(input("Ruch {}. Podaj kolumne!".format(player)))
            y = int(input("Ruch {}. Podaj wiersz!".format(player)))
        except:
            print("nie wiem co chciales osiagnac, ale tracisz ture")
        try:
            self.do_move(x - 1, y - 1, player)
        except:
            print("sorrki, spoza zakresu")

    def __prepare_map(self):
        for i in range(self.height):
            for n in range(self.width):
                self.position[i, n] = "-"


try:
    width = int(input("podaj szerokosc planszy(tak przynajmniej z 4): "))
    height = int(input("podaj wysokosc planszy(tak przynajmniej ze 4): "))
except:
    width = random.randint(4, 8)
    height = random.randint(4, 8)
    print("nie kumasz to ja ci wybiore. szerokość to {}, a wysokosc {}".format(width, height))

game = XOGame(width, height)
result = True


while result == True:
    game.make_round()
    game.draw_map()
    draw_flag = game.is_map_full()
    result = game.check_win()


if draw_flag == "remis":
    print("No niestety, remis.")
print("Koniec gry!")
