from typing import Optional
from game_display import GameDisplay
from apple import Apple
import math
from wall import Wall


class SnakeGame:

    def __init__(self) -> None:
        self.__orientation = "vertical"
        self.__key_clicked = None
        self.round = 0
        self.coordinates = []
        self.directions = ["Up", "Down", "Left", "Right"]
        self.current_dir = "Up"

    def snake_beginning(self, width, height):
        self.__y = height//2
        self.__x = width//2
        self.coordinates.append((self.__x, self.__y - 2))
        self.coordinates.append((self.__x, self.__y - 1))
        self.coordinates.append((self.__x, self.__y))

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def update_objects(self) -> None:
        if (self.__key_clicked == 'Up' and self.__orientation == "horizontal") or self.current_dir == "Up":
            self.coordinates.sort(key=lambda x: x[1])
            self.coordinates.remove(self.coordinates[0])
            new_head = self.coordinates[-1]
            y = new_head[1] + 1
            self.coordinates.append((new_head[0], y))
            self.__orientation = "vertical"

        elif (self.__key_clicked == 'Down' and self.__orientation == "horizontal") or self.current_dir == "Down":
            self.coordinates.sort(key=lambda x: x[1], reverse=True)
            self.coordinates.remove(self.coordinates[0])
            new_head = self.coordinates[-1]
            y = new_head[1] - 1
            self.coordinates.append((new_head[0], y))
            self.__orientation = "vertical"

        elif (self.__key_clicked == 'Right' and self.__orientation == "vertical") or self.current_dir == "Right":

            self.coordinates.sort(key=lambda x: x[0])
            self.coordinates.remove(self.coordinates[0])
            new_head = self.coordinates[-1]
            x = new_head[0] + 1
            self.coordinates.append((x, new_head[1]))
            self.__orientation = "horizontal"

        elif (self.__key_clicked == 'Left' and self.__orientation == "vertical") or self.current_dir == "Left":
            self.coordinates.sort(key=lambda x: x[0], reverse=True)
            self.coordinates.remove(self.coordinates[0])
            new_head = self.coordinates[-1]
            x = new_head[0] - 1
            self.coordinates.append((x, new_head[1]))
            self.__orientation = "horizontal"

    def draw_board(self, gd: GameDisplay) -> None:
        for cell in self.coordinates:
            gd.draw_cell(cell[0], cell[1], "black")

    def end_round(self) -> None:
        self.round += 1
        if self.__key_clicked == None:
            pass
        else:
            if self.current_dir == "Up" and self.__key_clicked != "Down":
                self.current_dir = self.__key_clicked
            elif self.current_dir == "Down" and self.__key_clicked != "Up":
                self.current_dir = self.__key_clicked
            elif self.current_dir == "Right" and self.__key_clicked != "Left":
                self.current_dir = self.__key_clicked
            elif self.current_dir == "Left" and self.__key_clicked != "Right":
                self.current_dir = self.__key_clicked

    def head_in_body(self):
        """
        Returns True if the snake's head hits his body, False if else
        """
        head = self.coordinates[-1]
        for cell in self.coordinates[:-1]:
            if cell == head:
                return True
        return False

    def out_of_bounds(self, width, height):
        """
        Returns True if the snake's head is out of the board, False if else
        """
        new_coor_list = []
        head = self.coordinates[-1]
        cond1 = head[0] < 0 and self.current_dir == "Left"
        cond2 = head[0] == width and self.current_dir == "Right"
        cond3 = head[1] == height and self.current_dir == "Up"
        cond4 = head[1] < 0 and self.current_dir == "Down"
        if cond1 or cond2 or cond3 or cond4:
            self.coordinates.remove(self.coordinates[-1])
            return True
        return False

    def eat_an_apple(self, apple: Apple):
        """
        Returns True if snake eats an apple
        """
        length = len(self.coordinates)
        score = 0
        head = self.coordinates[-1]
        if head in apple.apple_list:
            apple.apple_list.remove(head)
            score = math.floor(math.sqrt(length))
            return True, score
        return False, score

    def add_head(self):
        """
        Adds a new head to the snake
        """
        if self.current_dir == "Up":
            self.coordinates.sort(key=lambda x: x[1])
            new_head = self.coordinates[-1]
            y = new_head[1] + 1
            self.coordinates.append((new_head[0], y))

        elif self.current_dir == "Down":
            self.coordinates.sort(key=lambda x: x[1], reverse=True)
            new_head = self.coordinates[-1]
            y = new_head[1] - 1
            self.coordinates.append((new_head[0], y))

        elif self.current_dir == "Right":
            self.coordinates.sort(key=lambda x: x[0])
            new_head = self.coordinates[-1]
            x = new_head[0] + 1
            self.coordinates.append((x, new_head[1]))

        elif self.current_dir == "Left":
            self.coordinates.sort(key=lambda x: x[0], reverse=True)
            new_head = self.coordinates[-1]
            x = new_head[0] - 1
            self.coordinates.append((x, new_head[1]))

    def head_to_wall(self, wall: Wall):
        head = self.coordinates[-1]
        for wall in wall.walls_list:
            if head in wall:
                return True
        return False

    def is_over(self) -> bool:
        return False

# python C:\Users\ashta\OneDrive\Desktop\Intro\Exercises\ex10\game_display.py -a 100
