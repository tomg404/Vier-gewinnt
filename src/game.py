import os
import sys
import argparse
import time
import numpy as np
import colorama as c
from termcolor import cprint
from pyfiglet import figlet_format
from . import __version__, __author__

class Game:
    def __init__(self):
        c.init()    # initialize colorama to make colored output work on windows

        self.verbose = self.parse_args().verbose
        self.vprint = print if self.verbose else lambda *a, **k: None # thanks to https://stackoverflow.com/a/5980173/10653517 for this solution
        self.no_color = self.parse_args().no_color

        # toggle colored output
        if self.no_color:
            self.player1 = 'X'
            self.player2 = 'O'
        else:
            self.player1 = c.Fore.RED + 'X' + c.Style.RESET_ALL
            self.player2 = c.Fore.BLUE + 'O' + c.Style.RESET_ALL

        self.version = __version__
        self.sleep_time_at_start = 3
        self.empty = ' '
        self.current_player = 1
        self.user_input = 0
        self.field = [[self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty],
                    [self.empty,self.empty,self.empty,self.empty,self.empty,self.empty,self.empty]]


    def parse_args(self):
        parser = argparse.ArgumentParser(description='4 connects game in python', epilog='(c) %s'%__author__)
        parser.add_argument('-v', '--verbose', action='store_true', help='show which win check triggered on win')
        parser.add_argument('-nc', '--no-color', action='store_true', help='don\'t output color')
        args = parser.parse_args()
        return args

    def run(self):
        self.clear_screen()
        cprint(figlet_format('4 connects', font='slant'))

        for i in range(self.sleep_time_at_start):
            sys.stdout.write("Game starting in: %d \r" % (self.sleep_time_at_start - i) )
            sys.stdout.flush()
            time.sleep(1)

        self.clear_screen()
        won = False
        while True:
            try:
                self.print_field()
                self.get_user_input()
                self.insert()
                self.clear_screen()
                won = self.check_win()
                if won:
                    self.print_field()
                    print('You won!')
                    break
            except KeyboardInterrupt:
                text = 'Game ended'
                if self.no_color:
                    print(text)
                else:
                    print(c.Fore.RED + text + c.Style.RESET_ALL)
                sys.exit()

    def print_field(self):
        tabs = '            '
        credits = ' 4 Connects (v%s) (c) Tom Gaimann 2019 ' % self.version
        print('╔' + len(credits) * '═' + '╗')
        print('║' + credits + '║')
        print('╚' + len(credits) * '═' + '╝')

        print(tabs + '╔═══════════════╗')
        print(tabs + '║|0|1|2|3|4|5|6|║')
        for i in range(0, 6):
            print(tabs + '║|{}|{}|{}|{}|{}|{}|{}|║'.format(self.field[i][0],self.field[i][1],self.field[i][2],self.field[i][3],self.field[i][4],self.field[i][5],self.field[i][6]))
        print(tabs + '╚═══════════════╝')

    def get_user_input(self):
        try:
            self.user_input = int(input('Choose column Player {}: '.format(self.current_player)))
        except ValueError:
            print('Invalid input. Try again!')
            self.get_user_input()

        # check if user input exceeds value and if the top field is not empty
        if self.user_input > 6 or self.user_input < -7 or self.field[0][self.user_input] != self.empty:
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

        self.vprint("  Linear check: %s" % l)
        self.vprint("Vertical check: %s" % v)
        self.vprint("Diagonal check: %s" % d)

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
        # function for checking the array
        def check_array(array):
            for col in range(0, 7):
                win_diag = np.diagonal(array, col)
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

        # convert array to numpy array
        win_arr = np.array(self.field)

        # check every diagonal from up to down if there are 4 of the same
        if check_array(win_arr):
            self.vprint('_check_win_diagonal::check_array::1')
            return True

        # flip array and again check every diagonal if there are 4 of the same
        win_arr = np.fliplr(win_arr)
        if check_array(win_arr):
            self.vprint('_check_win_diagonal::check_array::2')
            return True

        # flip array upside down
        win_arr = np.flipud(win_arr)
        if check_array(win_arr):
            self.vprint('_check_win_diagonal::check_array::3')
            return True

        # flip array left to right again
        win_arr = np.fliplr(win_arr)
        if check_array(win_arr):
            self.vprint('_check_win_diagonal::check_array::4')
            return True


        # if there are no matching chars return False
        return False
