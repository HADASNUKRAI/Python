from game_display import GameDisplay
from game_utils import *
from apple import Apple


class Wall:
    def __init__(self) -> None:
        self.walls_list = []

    def add_wall(self, gd: GameDisplay):
        single_wall = []
        x, y, direction = get_random_wall_data()
        if direction == "Up" or direction == "Down":
            single_wall.append((x, y-1))
            single_wall.append((x, y))
            single_wall.append((x, y+1))
        elif direction == "Right" or direction == "Left":
            single_wall.append((x-1, y))
            single_wall.append((x, y))
            single_wall.append((x+1, y))
        single_wall.append(direction)

        for cell in gd._already_drawn:
            gd_cell = (cell[0], cell[1])
            if gd_cell in single_wall:
                return False
        self.walls_list.append(single_wall)
        return True

    def draw_walls(self, gd: GameDisplay) -> None:
        for wall in self.walls_list:
            for coor in range(3):
                if wall[coor][0] in range(gd.width) and wall[coor][1] in range(gd.height):
                    gd.draw_cell(wall[coor][0], wall[coor][1], "blue")

    def remove_wall(self, gd: GameDisplay):
        walls_to_remove = []
        for wall in self.walls_list:
            cell_counter = 0
            for cell in range(3):
                if wall[cell][0] in range(gd.width) and wall[cell][1] in range(gd.height):
                    cell_counter += 1
            if cell_counter == 0:
                walls_to_remove.append(wall)

        for member in walls_to_remove:
            self.walls_list.remove(member)

        return len(walls_to_remove)

    def move_walls(self):
        for single_wall in self.walls_list:
            direction = single_wall[3]
            if direction == "Up":
                single_wall[0] = (single_wall[0][0], single_wall[0][1] + 1)
                single_wall[1] = (single_wall[1][0], single_wall[1][1] + 1)
                single_wall[2] = (single_wall[2][0], single_wall[2][1] + 1)
            elif direction == "Down":
                single_wall[0] = (single_wall[0][0], single_wall[0][1] - 1)
                single_wall[1] = (single_wall[1][0], single_wall[1][1] - 1)
                single_wall[2] = (single_wall[2][0], single_wall[2][1] - 1)
            elif direction == "Right":
                single_wall[0] = (single_wall[0][0] + 1, single_wall[0][1])
                single_wall[1] = (single_wall[1][0] + 1, single_wall[1][1])
                single_wall[2] = (single_wall[2][0] + 1, single_wall[2][1])
            elif direction == "Left":
                single_wall[0] = (single_wall[0][0] - 1, single_wall[0][1])
                single_wall[1] = (single_wall[1][0] - 1, single_wall[1][1])
                single_wall[2] = (single_wall[2][0] - 1, single_wall[2][1])

    def wall_head(self, single_wall):
        curr_dir = single_wall[3]
        if curr_dir == "Up" or curr_dir == "Right":
            head = single_wall[2]
        elif curr_dir == "Down" or curr_dir == "Left":
            head = single_wall[0]

        return head

    def destroy_an_apple(self, apple: Apple):
        """
        Returns True if the wall crashes into an apple
        """
        apples_removed = 0
        for single_wall in self.walls_list:
            head = self.wall_head(single_wall)

            if head in apple.apple_list:
                apple.apple_list.remove(head)
                apples_removed += 1
        return apples_removed

    def wall_to_snake(self, coordinates):
        for single_wall in self.walls_list:
            head = self.wall_head(single_wall)
            if head in coordinates:
                crash_index = coordinates.index(head)
                deleted_cells = coordinates[:crash_index + 1]
                remain_cells = coordinates[crash_index + 1:]
                return deleted_cells, remain_cells
        return None, None
