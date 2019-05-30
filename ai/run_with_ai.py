from game_with_ai import Game
from ai import Ai
import time
import random

g = Game(True)
won = False

while True:
    g.print_field()
    if g.current_player == 2:
        print('AI is on the turn!')
        time.sleep(0.5)
        current_field = g.get_field()
        last_input = g.get_last_user_input()

        ai = Ai(current_field, last_input)
        column = ai.calculate()
        g.get_user_input(column)
    else:
        g.get_user_input()

    g.clear_screen()
    g.insert()
    won = g.check_win()


    if won == True:
        g.print_field()
        break
