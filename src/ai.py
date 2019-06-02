import numpy as np
import random
class Ai:

    def __init__(self, field, last_input, turns):
        self.field = field
        self.last_input = last_input
        self.turns = 0

    def calculate(self):
        return random.randint(0, 7)

    def __check_for_first_turn(self):
        pass

    def __check_for_field_end(self):
        pass

    def __check_for_3_in_a_row(self):
        pass
