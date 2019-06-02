import numpy as np
import random

class Ai:
    def __init__(self, field, last_input, turns):
        self.field = field
        self.last_input = last_input
        self.turns = 0
        self.player1 = "X"
        self.player2 = "O"
        self.empty = " "

    def calculate(self):
        if self.last_input >= 6:
            return self.last_input
        elif self.last_input <= 0:
            return self.last_input
        else:
            return self.last_input + 1

    def __check_for_first_turn(self):
        pass

    def __check_for_field_end(self):
        pass

    def __check_for_3_in_a_row(self):
        for i in range(0, 6):
            win_row = str(self.field[i]).replace(",","").replace("'","").replace("[","").replace("]","").replace(" ", ".")

            if (2*(self.player1 + ".")+self.player1) in win_row:
                print("detected 3 in a row")
                return True
