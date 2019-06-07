"""Modified version of the original game class"""
import os
import time
import numpy as np
from src.game import Game

class Game_ai(Game):
    def get_field(self):
        return self.field

    def get_current_player(self):
        return self.current_player

    def get_last_user_input(self):
        return self.user_input

    def get_user_input(self, ai=None):
        if ai is not None:
            print("AI is on the turn")
            time.sleep(0.5)
            self.user_input = ai
        else:
            try:
                self.user_input = int(input('Choose column Player {}: '.format(self.current_player)))
            except ValueError:
                print('Invalid input. Try again!')
                self.get_user_input()

            if self.user_input > 6 or self.user_input < -7:
                print('Invalid input. Try again!')
                self.get_user_input()
