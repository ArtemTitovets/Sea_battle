import random


class Dot:
    mimo_shot = '| T '
    hit_shot = '| X '
    svob_dot = '| 0 '
    ship_dot = '| ■ '
    ship_cont = '| . '

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:

    def __init__(self, x, y, length, direction, ship_dot=None):
        self.x = x
        self.y = y
        self.length = length
        self.number_lives = length
        self.direction = direction
        self.ship_dot = ship_dot
        if ship_dot is None:
            ship_dot = []
        self.ship_contur = []

    def dots(self):
        self.ship_dot = []
        if self.direction == 1:
            for dot in range(self.length):
                self.ship_dot.append(Dot(self.x - 1 + dot, self.y - 1))
        else:
            for dot in range(self.length):
                self.ship_dot.append(Dot(self.x - 1, self.y - 1 + dot))
        return self.ship_dot

    def ship_cont(self, ship_dot):
        for dot in self.ship_dot:
            for i in range(dot.x - 1, dot.x + 2):
                for j in range(dot.y - 1, dot.y + 2):
                    if Dot(i, j) not in self.ship_contur and \
                        Dot(i, j) not in self.ship_dot and \
                        0 <= i <= 5 and 0 <= j <= 5:
                        self.ship_contur = self.ship_contur + [Dot(i, j)]
        return self.ship_contur


class Board:

    def __init__(self, hid=False):
        self.board = [[Dot.svob_dot] * 6 for _ in range(6)]
        self.live_ships = []
        self.busy_dot = []
        self.shots = []
        self.hid = hid
        self.ships_hp = 0

    def __str__(self):
        for i in range(7):
            if i == 0:
                i = ""
            print('|', i, end=" ")
        print('\n''--------------------------')
        for i in range(6):
            for j in range(6):
                if j == 0:
                    print(i + 1, '', self.board[i][j], end="")
                else:
                    print(self.board[i][j], end="")
            print()
        return self.board

    def add_ships(self, ship, hid=True):
        try:
            for dot in ship.dots():
                if dot in self.busy_dot or dot.x < 0 or dot.x > 5 or dot.y < 0 or dot.y > 5:
                    raise IndexError
            for dot in ship.dots():
                if hid == True:
                    self.board[dot.x][dot.y] = dot.ship_dot
                else:
                    self.board[dot.x][dot.y] = dot.svob_dot
            self.live_ships.append(ship)
            self.ships_hp += ship.length
            self.busy_dot = self.busy_dot + ship.dots()
            self.busy_dot = self.busy_dot + ship.ship_cont(ship.dots())
            return self.board, self.live_ships, self.busy_dot
        except IndexError:
            if hid is True:
                print('Ошибка в расположении корабля!')
            return False
        return self.ships_hp

    def shot(self, cord, hid=True):
        try:
            shot = Dot((cord.x), (cord.y))
            if shot.x < 0 or (cord.x) > 6 or (cord.y) < 0 or (cord.y) > 6 or \
                    Dot((cord.x), (cord.y)) in self.shots or \
                    self.board[(cord.x)][(cord.y)] == Dot.ship_cont:
                raise IndexError
            try:
                for ship in self.live_ships:
                    for dot in ship.dots():
                        if shot in ship.dots():
                            self.board[(cord.x)][(cord.y)] = Dot.hit_shot
                            self.ships_hp -= 1
                            ship.number_lives -= 1
                            if ship.number_lives == 0:
                                for dot in ship.ship_contur:
                                    self.board[dot.x][dot.y] = Dot.ship_cont
                                    self.shots = self.shots + [Dot((cord.x), (cord.y))]
                            raise StopIteration
                        else:
                            self.board[(cord.x)][(cord.y)] = Dot.mimo_shot
                            self.shots = self.shots + [Dot((cord.x), (cord.y))]
            except StopIteration:
                pass
        except IndexError:
            if hid is True:
                print('Ошибка выстрела, повторите выстрел!')
                raise IndexError
        return self.shots


class Player:
    def __init__(self, board_player, board_ii):
        self.board_player = board_player
        self.board_ii = board_ii

    @staticmethod
    def ask():
        raise NotImplementedError('Метод ask будет реализован подклассами')

    def move(self):
            try:
                target = self.ask()
                return target
            except ValueError as e:
                print(e)


class User(Player):
    @staticmethod
    def ask():
        while True:
            try:
                x = int(input('Введите № строки: '))
                y = int(input('Введите № столбца: '))
                cord = Dot(x - 1, y - 1)
                return cord
            except ValueError:
                print('Неверные координаты. Пожалуйста, повторите ввод.')


class II(Player):
    def ask(self):
        cord = Dot
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return cord(x, y)


class Game:
    def __init__(self, shot=None):
        self.ship_length_list = [3, 2, 2, 1, 1, 1, 1]
        self.shot = shot

    def gen_player_board(self):
        board_player = Board()
        board_player.__str__()
        ship_count_player = 0
        while ship_count_player != 7:
            try:
                x = int(input('Введите № строки: '))
                y = int(input('Введите № столбца: '))
                length = self.ship_length_list[ship_count_player]
                if length == 1:
                    direction = 1
                else:
                    direction = int(input("положение: "))
                ship = Ship(x, y, length, direction)
                if bool(board_player.add_ships(ship)) == True:
                    ship_count_player += 1
                    print('Поле игрока:')
                    board_player.__str__()
                    print()
            except IndexError:
                print('Вы ввели неверные координаты!')
            except ValueError:
                print('Вы ввели неверные координаты!')
        else:
            return board_player

    def gen_ii_board(self):
        board_ii = Board()
        ship_count = 0
        ship_count_ii = 0
        while ship_count_ii != 7:
            x = random.randint(1, 6)
            y = random.randint(1, 6)
            length = self.ship_length_list[ship_count_ii]
            if length == 1:
                direction = 1
            else:
                direction = random.randint(1, 3)
            ship = Ship(x, y, length, direction)
            if bool(board_ii.add_ships(ship, hid=False)) == True:
                ship_count_ii += 1
            else:
                ship_count += 1
                if ship_count > 1000:
                    ship_count = 0
                    ship_count_ii = 0
                    board_ii = Board()
                    return Start_game.gen_ii_board()
        else:
            return board_ii

    def loop(self):
        print(' ПРИВЕТСТВУЮ!!!\n Перед началом игры прошу ознакомиться с правилами:\n'
              '\n'
              ' При запуске игры появится доска игрока, вам следует расставить корабли на доске.\n'
              ' Расстановка производится в следующем порядке:\n'
              ' Один 3-ёх палубный\n'
              ' Два 2-ух палубных\n'
              ' Четыре 1-но палубных\n'
              '\n'
              ' Для расстановки следует ввести координаты строки и столбца (используйте цифры от 1 до 6)\n'
              ' В поле положение корабля для вертикального размещения введите: 1, для горизонтального: 2\n'
              ' Вертикальное размещение происходит вниз от заданной коардинаты, горизонтальное вправо,\n'
              ' для 1-но палубных кораблей положение вводить не требуется.\n'
              '\n'
              ' корабли следует размещать на расстоянии минимум 1 клетки друг от друга!!!\n'
              '\n'
              ' Пебеждает тот, кто первым уничтожит все корабли проивника!\n'
              '\n'
              ' УДАЧНОЙ ИГРЫ!!!')

    def start(self, board_player, board_ii):
        self.board_player = board_player
        self.board_ii = board_ii
        print('Поле ИИ:')
        self.board_ii.__str__()
        print('Начинаем игру!!!')

        ai = II(self.board_ii, self.board_player)
        pl = User(self.board_player, self.board_ii)
        paluba_ii = 11
        paluba_pl = 11
        while True:
            while True:
                try:
                    self.board_ii.shot(pl.move())
                    if paluba_ii != self.board_ii.ships_hp:
                        print()
                        print('Вы поразили врага, повторите выстрел!')
                        self.board_ii.__str__()
                        paluba_ii -= 1
                        if paluba_ii == 0:
                            break
                    else:
                        print('Вы промахнулись')
                        self.board_ii.__str__()
                        print()
                        print('Ход ИИ: ')
                        break
                except IndexError:
                    print('Вы ввели неверные координаты!')
                    self.board_ii.__str__()
                except ValueError:
                    print('Неверный выстрел!')
                    self.board_ii.__str__()
            while True:
                try:
                    self.board_player.shot(ai.move(), hid = False)
                    if paluba_pl != self.board_player.ships_hp:
                        print('Враг подбил ваш корабль')
                        self.board_player.__str__()
                        print('Повторный выстрел:')
                        paluba_pl -= 1
                        if paluba_pl == 0:
                            break
                    else:
                        self.board_player.__str__()
                        print()
                        print('ИИ промахнулся')
                        print('Ваш ход: ')
                        self.board_ii.__str__()
                        break
                except IndexError:
                    None
                except ValueError:
                    None
            if self.board_ii.ships_hp == 0:
                print('Поздравляю! ИИ разгромлен!!!')
                continue
            if self.board_player.ships_hp == 0:
                print('Увы, Вы проиграли!')
                continue

Start_game = Game()
Start_game.loop()
Start_game.start(Start_game.gen_player_board(), Start_game.gen_ii_board())