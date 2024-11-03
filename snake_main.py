import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
from apple import Apple
from wall import Wall


def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    gd._already_drawn = {}
    args_dict = vars(args)
    input_round = args_dict['rounds']
    input_walls = args_dict['walls']
    # INIT OBJECTS
    apples_eaten = 0
    ver_added = 0
    num_of_walls = 0
    wall = Wall()
    game = SnakeGame()
    apple = Apple()
    game.snake_beginning(args_dict['width'], args_dict['height'])
    if wall.add_wall(gd):
        num_of_walls += 1
    apple.add_apple(gd)
    gd.show_score(0)
    # DRAW BOARD
    game.draw_board(gd)
    wall.draw_walls(gd)
    apple.draw_apples(gd)
    gd.end_round()
    if input_round == 0:
        quit()
    # END OF ROUND 0
    while not game.is_over():
        # CHECK KEY CLICKS
        if game.round > input_round and input_round > 0:
            quit()
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        if game.round + 1 < args_dict['apples']:
            apple.add_apple(gd)
        # DRAW BOARD
        game.draw_board(gd)
        wall.draw_walls(gd)
        apple.draw_apples(gd)
        deleted_cell, remain_cells = wall.wall_to_snake(game.coordinates)
        if deleted_cell != None and remain_cells != None:
            game.coordinates = remain_cells
            remained_dict = {}
            for cell in gd._to_draw:
                if not cell in deleted_cell:
                    remained_dict[cell] = gd._to_draw[cell]
            gd._to_draw = remained_dict
            game.draw_board(gd)

        if game.head_to_wall(wall):
            new_dict = {}
            for key in gd._to_draw:
                if gd._to_draw[key] != "black":
                    new_dict[key] = gd._to_draw[key]
            gd._to_draw = new_dict
            game.coordinates = []
            game.draw_board(gd)
            gd.end_round()
            quit()
        is_eating, score = game.eat_an_apple(apple)
        if is_eating:
            apples_eaten += 3
            gd.show_score(score)
        if ver_added < apples_eaten:
            game.add_head()
            ver_added += 1
        is_out = game.out_of_bounds(
            args_dict['width'], args_dict['height'])
        if game.head_in_body() or is_out:
            game.draw_board(gd)
            for drawn in gd._to_draw:
                if gd._to_draw[drawn] == "black":
                    if not drawn in game.coordinates:
                        del gd._to_draw[drawn]
                        break
            gd.end_round()
            quit()
        if game.round % 2 == 0:
            wall.move_walls()
        wall.destroy_an_apple(apple)
        walls_removed = wall.remove_wall(gd)
        num_of_walls -= walls_removed
        if num_of_walls < input_walls and game.round > input_round:
            if walls_removed == 0:
                walls_removed += 1
            for i in range(walls_removed):
                wall.add_wall(gd)
                num_of_walls += 1
        missing_apples = args_dict['apples'] - len(apple.apple_list)
        if len(apple.apple_list) < args_dict['apples'] and game.round > args_dict['apples']:
            for j in range(missing_apples):
                apple.add_apple(gd)
            apple.draw_apples(gd)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        gd.end_round()


if __name__ == "__main__":
    print("You should run:\n"
          "> python game_display.py")
