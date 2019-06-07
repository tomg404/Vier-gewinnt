import os
import argparse
import numpy as np

class Game:
    def __init__(self):
        self.version = '1.1'
        self.empty = ' '
        self.player1 = 'X'
        self.player2 = 'O'
        self.current_player = 1
        self.user_input = 0
        self.field = [[self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty]]
        self.verbose = self.parse_args().verbose

    def parse_args(self):
        parser = argparse.ArgumentParser(description='4 connects game in python')
        parser.add_argument('-v', '--verbose', action='store_true', help='show which win check triggered on win')
        args = parser.parse_args()
        return args

    def run(self):
        won = False
        while True:
            self.print_field()
            self.get_user_input()
            self.insert()
            self.clear_screen()
            won = self.check_win()
            if won:
                self.print_field()
                break

    def print_field(self):
        print('4 Connects (v%s) (c) Tom Gaimann 2019' % self.version)
        print('|0|1|2|3|4|5|6|')
        for i in range(0, 6):
            print('|{}|{}|{}|{}|{}|{}|{}|'.format(self.field[i][0],self.field[i][1],self.field[i][2],self.field[i][3],self.field[i][4],self.field[i][5],self.field[i][6]))

    def get_user_input(self):
        try:
            self.user_input = int(input('Choose column Player {}: '.format(self.current_player)))
        except ValueError:
            print('Invalid input. Try again!')
            self.get_user_input()

        if self.user_input > 6 or self.user_input < -7:
            print('Invalid input. Try again!')
            self.get_user_input()

    def insert(self):
        column = self.user_input
        lowestVal = 5
        while True:
            if lowestVal < 0:
                break
            elif self.field[lowestVal][column] == self.empty:
                break
            else:
                lowestVal -= 1

        if self.current_player == 1 and self.field[lowestVal][column] is not self.player2:
            self.field[lowestVal][column] = self.player1
            self.change_player()

        if self.current_player == 2 and self.field[lowestVal][column] is not self.player1:
            self.field[lowestVal][column] = self.player2
            self.change_player()

    def change_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def clear_screen(self):
        # windows & linux compatible
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def check_win(self):

        l = self._check_win_linear()
        v = self._check_win_vertical()
        d = self._check_win_diagonal()

        if self.verbose == True:
            print("  Linear check: %s" % l)
            print("Vertical check: %s" % v)
            print("Diagonal check: %s" % d)

        if l == True or v == True or d == True:
            return True
        else:
            return False

    def _check_win_linear(self):
        # linear check
        for i in range(0, 6):
            # converts array into string (e.g. ['x','x','x'] -> xxx)
            win_row = str(self.field[i]).replace(",","").replace("'","").replace("[","").replace("]","").replace(" ", ".")

            # checks if 4 same characters are in a row
            if (3*(self.player1 + ".")+self.player1) in win_row:
                print("Player 1 won")
                return True
            elif (3*(self.player2 + ".")+self.player2) in win_row:
                print("Player 2 won")
                return True

        return False

    def _check_win_vertical(self):
        # vertical check
        win_arr = np.array(self.field)
        for col in range(0, 7):
            #                [:,col]  get first item from every list
            win_col = str(win_arr[:,col]).replace(",","").replace("'","").replace("[","").replace("]","").replace(" ", ".")
            # checks for every "win_col" if it contains 4 of the same chars
            if 3*(self.player1+".")+self.player1 in win_col:
                print("Player 1 won")
                return True
            elif 3*(self.player2+".")+self.player2 in win_col:
                print("Player 2 won")
                return True
            # reset win_col
            win_col = ""

        return False

    def _check_win_diagonal(self):
            # convert array to numpy array
            win_arr = np.array(self.field)

            # check every diagonal if there are 4 of the same
            for col in range(0, 7):
                win_diag = np.diagonal(win_arr, col)
                if len(win_diag) < 4:
                    pass
                else:
                    win_diag, counts = np.unique(win_diag, return_counts=True)
                    win_dict = dict(zip(win_diag, counts))
                    try:
                        if win_dict[self.player1] == 4:
                            return True
                        elif win_dict[self.player2] == 4:
                            return True
                    except KeyError:
                        pass

            # flip array and again check every diagonal if there are 4 of the same
            win_arr = np.fliplr(win_arr)
            for col in range(0, 7):
                win_diag = np.diagonal(win_arr, col)
                if len(win_diag) < 4:
                    pass
                else:
                    win_diag, counts = np.unique(win_diag, return_counts=True)
                    win_dict = dict(zip(win_diag, counts))
                    try:
                        if win_dict[self.player1] == 4:
                            return True
                        elif win_dict[self.player2] == 4:
                            return True
                    except KeyError:
                        pass

            # if there are no matching chars return False
            return False
