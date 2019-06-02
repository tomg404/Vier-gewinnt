from src.game_ai import Game_ai
from src.ai import Ai
import random

game = Game_ai(True)
won = False
turns = 0   # count turns

while True:
    game.print_field()
    print('Turns: ', turns)
    if game.current_player == 2:

        current_field = game.get_field()
        last_input = game.get_last_user_input()

        ai = Ai(current_field, last_input, turns)
        column = ai.calculate()
        game.get_user_input(column)

    else:
        game.get_user_input()

    game.clear_screen()
    game.insert()
    won = game.check_win()
    if won == True:
        game.print_field()
        break
    # increase turn counter
    turns += 1
