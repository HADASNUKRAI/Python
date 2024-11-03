from game_utils import *
from game_display import GameDisplay


class Apple:

    COLOR_LIST = ["black", "green", "blue"]

    def __init__(self):
        self.apple_list = []

    def add_apple(self, gd: GameDisplay):
        x, y = get_random_apple_data()
        for cell in gd._already_drawn:
            if x == cell[0] and y == cell[1]:
                return
        self.apple_list.append((x, y))

    def draw_apples(self, gd: GameDisplay) -> None:
        for apple in self.apple_list:
            gd.draw_cell(apple[0], apple[1], "green")
