import os

class Game:
    def __init__(self, verbose):
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
        self.verbose = False

    def run(self):
        won = False
        while True:
            self.clear_screen()
            self.print_field()
            self.get_user_input()
            self.insert()
            won = self.check_win()
            if won:
                self.print_field()
                break

    def print_field(self):
        print()
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
            print("Linear check: %s" % l)
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
            win_row = str(self.field[i]).replace(",","").replace("'","").replace("[","").replace("]","")

            # checks if 4 same characters are in a row
            if 4 * (self.player1 + " ") in win_row:
                print("Player 1 won")
                return True
            elif 4 * (self.player2 + " ") in win_row:
                print("Player 2 won")
                return True

    def _check_win_vertical(self):
        # vertical check
        win_col = ""
        for col in range(0, 7):
            for row in range(0, 6):
                win_col += str(self.field[row][col]).replace("',","").replace("[","").replace("]","").replace(" ", "").replace("'", "")

            # checks for every "win-string" if it contains 4 of the same chars
            if 4 * self.player1 in win_col:
                print("Player 1 won")
                return True
            elif 4 * self.player2 in win_col:
                print("Player 2 won")
                return True

            # reset win_col
            win_col = ""

    def _check_win_diagonal(self):
        # diagonal check
        # explanation: the algorithm searches from a field in a radius of 4 every possible field.
        #              if the algorithm finds 4 matching characters in a row it returns true (ends the program)
        win_diag = ""
        f = self.field
        matching = 1
        for col in range(0,7):
            for row in range(0,6):
                for n in range(1,5):
                    try:
                        # if statement for player 1 up right check
                        if f[row][col] == self.player1 and f[row][col] == f[row-n][col+n]:
                            #print('found match:', row, col, 'and', row-n, col+n)
                            matching += 1   # increments the match counter
                        elif matching == 4:
                            print("Player 1 won")
                            return True
                        else:
                            matching = 1    # reset the match counter
                    except:
                        pass
                #########################################################
                for n in range(1,5):
                    try:
                        # if statement for player 2 up right check
                        if f[row][col] == self.player2 and f[row][col] == f[row-n][col+n]:
                            matching += 1
                        elif matching == 4:
                            print("Player 2 won")
                            return True
                        else:
                            matching = 1
                    except:
                        pass
                #########################################################
                for n in range(1,5):
                    try:
                        # if statement for player 2 up right check
                        if f[row][col] == self.player1 and f[row][col] == f[row-n][col-n]:
                            matching += 1
                        elif matching == 4:
                            print("Player 1 won")
                            return True
                        else:
                            matching = 1
                    except:
                        pass
                #########################################################
                for n in range(1,5):
                    try:
                        # if statement for player 2 up right check
                        if f[row][col] == self.player2 and f[row][col] == f[row-n][col-n]:
                            matching += 1
                        elif matching == 4:
                            print("Player 2 won")
                            return True
                        else:
                            matching = 1
                    except:
                        pass
