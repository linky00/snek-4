import unittest
from unittest.mock import patch

class Tests (unittest.TestCase):
    def setUp (self):
        pass

    def test_game (self):
        self.game = Game('yellow', [7,6])
        self.game.take_turn(player_input=1)
        self.assertTrue(self.game.turns[0].drop_location == [0,5])

    def test_invalid (self):
        self.game = Game('yellow', [7,6])
        self.game.take_turn(player_input="boop")
        self.assertTrue(len(self.game.turns) == 0)

    def test_board_icons (self):
        self.empty_board = Board([2,2])
        self.assertTrue(self.empty_board.board_icons() == "..\n..\n--\n12")

    def test_game_logic (self):
        self.game = Game('yellow', [7,6])
        for x in [1, 5, 4, 3, 4, 4, 3, 2, 3, 2, 2, 1, 5, 1, 1]:
            self.game.take_turn(player_input=x)
        self.assertIs(self.game.victory, True)

    def test_check_icon (self):
        self.yellow_checker = Checker('yellow')
        self.red_checker = Checker('red')
        self.empty_checker = Checker('empty')
        self.assertIs(self.yellow_checker.icon, "X")
        self.assertIs(self.red_checker.icon, "O")
        self.assertIs(self.empty_checker.icon, ".")

class Game ():
    def __init__ (self, first_player, board_size):
        self.player = first_player
        self.board = Board(board_size)
        self.turns = []
        self.victory = False

    def play_game (self):
        while self.victory == False:
            print(self.board.board_icons())
            command = self.take_turn()
            if command == 'replay':
                self.replay(self.board.size, turns)
        print(self.board.board_icons())
        print(self.player + " victory!")

    def replay (self, board_size, turns):
        replay_board = Board(board_size)
        for turn in turns:
            replay_board.board[turn.drop_location[1]][turn.drop_location[0]] = Checker(turn.player)
            print(replay_board.board_icons())
            input("<enter to continue> ")

    def take_turn (self, player_input=None):
        if player_input == None:
            player_input = input("<" + self.player + "> ")
        if player_input == "replay":
            return 'replay'
        turn = self.board.drop_checker(self.player, player_input)
        if turn:
            self.turns.append(turn)
            if turn.victory == True:
                self.victory = True
            else:
                self.player = self.change_turns()
        if len(self.turns) == self.board.size[0] * self.board.size[1]:
            print("uh... the board's full.")
            self.victory = True

    def change_turns (self):
        if self.player == 'yellow':
            return 'red'
        return 'yellow'

class Turn ():
    def __init__ (self, drop_location, player, victory):
        self.drop_location = drop_location
        self.player = player
        self.victory = victory

class Board ():
    def __init__ (self, size):
        self.size = size
        self.board = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                row.append(Checker('empty'))
            self.board.append(row)

    def drop_checker (self, colour, location):
        try:
            location = int(location) - 1
        except ValueError:
            print("not a number :(")
            return None
        if not (0 <= location <= self.size[1]):
            print("not in range :(")
            return None
        rows_fallen = self.size[1] - 1
        for row in reversed(self.board):
            if row[location].colour == 'empty':
                row[location] = Checker(colour)
                for direction_pair in [[[0, 1], [0, -1]], [[1, 0], [-1, 0]], [[1, 1], [-1, -1]], [[1, -1], [-1, 1]]]:
                    connections = 0
                    for direction in direction_pair:
                        try:
                            connections += self.try_direction([location, rows_fallen], direction, colour, 0)
                        except IndexError:
                            pass
                    if connections >= 3:
                        return Turn([location, rows_fallen], colour, True)
                return Turn([location, rows_fallen], colour, False)
            rows_fallen -= 1
        print("row already full up")
        return None

    def try_direction (self, location, direction, colour, connections):
        test_location = [location[0] + direction[0], location[1] + direction[1]]
        try:
            if self.board[test_location[1]][test_location[0]].colour == colour:
                connections += self.try_direction (test_location, direction, colour, connections)
                connections += 1
        except IndexError:
            pass
        return connections

    def board_icons (self):
        output_as_list = []
        for row in self.board:
            row_output_as_list = list((checker.icon for checker in row))
            output_as_list.append(row_output_as_list)
        output = ""
        for row in output_as_list:
            row_output = ""
            for icon in row:
                row_output += icon
            output += row_output + "\n"
        for i in range(self.size[0]):
            output += "-"
        output += "\n"
        for i in range(1, self.size[0] + 1):
            output += str(i)
        output += "\n"
        return output

class Checker ():
    def __init__ (self, colour):
        self.colour = colour
        self.icon = {'yellow': "X", 'red': "O", 'empty': "."}[colour]

title = """
 _______  __    _  _______  ___   _      _   ___
|       ||  |  | ||       ||   | | |    | | |   |
|  _____||   |_| ||    ___||   |_| |    | |_|   |
| |_____ |       ||   |___ |      _|    |       |
|_____  ||  _    ||    ___||     |_     |___    |
 _____| || | |   ||   |___ |    _  |        |   |
|_______||_|  |__||_______||___| |_|        |___|

"""
instructions = """
welcome to snek 4, fun game for fun family

menu:
'play' to begin game and 'help' to read this again
'save <filename>' to save last game to file
'load <filename>' to replay game on file
if your name is ali sezer do 'unittest'
oh and 'quit' if you're bored...

in game:
first player is yellow (X) and second is red (O)
to place piece, enter number
to replay enter 'replay'
to exit enter 'exit'
"""
board_size = [7,6]

print(title)
print(instructions)
while True:
    command = input("<menu> ")
    if command == "play":
        game = Game('yellow', board_size)
        game.play_game()
    elif command == "help":
        print(instructions)
    elif command.startswith("save"):
        try:
            game_file = open('saves/' + command.split("save ", 1)[1], 'w+')
        except PermissionError:
            print("ya got to put a file name")
        try:
            for turn in game.turns:
                game_file.write(str(turn.drop_location) + turn.player + "\n")
            game_file.close()
            print("done!")
        except NameError:
            print("no game played!")
    elif command.startswith("load"):
        try:
            game_file = open('saves/' + command.split("load ", 1)[1], 'r')
        except PermissionError:
            print("ya got to put a file name")
        loaded_turns = []
        for line in game_file:
            # yes i know i could use regex here but i'm tired k
            line = line.rstrip()
            awful_numbers = line.split("]")
            messy_numbers = awful_numbers[0].split(", ")
            better_numbers = [int(messy_numbers[0].replace("[", "")), int(messy_numbers[1].replace("]", ""))]
            loaded_turns.append(Turn(better_numbers, awful_numbers[1], False))
        load_game = Game('yellow', board_size)
        load_game.replay(board_size, loaded_turns)
    elif command == "unittest":
        unittest.main()
    elif command == "quit":
        print("k bye")
        break
    else:
        print("not a command :(")
        print("do 'help' to hear the commands")
