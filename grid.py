import copy as cp
import random


def square(occupied=False, coin=None):
    """:return Dict that gives the cell properties and children"""
    if coin:
        occupied = True
    return {"occupied": occupied, "coin": coin, "coin_looker": False, "visited": False}


class State:

    def __init__(self, win_width=None, win_height=None, square_size=None):
        """ Init the grid as a dict where keys are coordinates and item the cell properties."""
        self.grid = dict()
        self.width = win_width
        self.height = win_height
        self.square_size = square_size
        if win_width and win_height and square_size:
            self.__set_cells(win_width, win_height, square_size)

    def __set_cells(self, win_width, win_height, square_size):
        """Init the cells of the grid according to the canvas size and the cell size.
        Default cell size is fixed as 50px."""
        for x in range(0, win_width, square_size):
            for y in range(0, win_height, square_size):
                # checks if the cell is occupied or not
                if random.random() >= 0.1:
                    cell = square()
                else:
                    cell = square(occupied=True)
                self.grid[(x, y)] = cell

    def __copy__(self):
        st = State()
        st.width, st.height, st.square_size = self.width, self.height, self.square_size
        st.grid = dict()
        for k, v in self.grid.items():
            st.grid[k] = cp.copy(v)

        return st

    def get_random_cell(self):
        """:return a random cell which is not occupied"""
        keys = list(self.grid.keys())
        random_key = keys[random.randint(0, len(keys) - 1)]
        while self.grid[random_key]["occupied"] or self.grid[random_key]["coin"]:
            random_key = keys[random.randint(0, len(keys) - 1)]
        return random_key

    def put_coin(self):
        """Put coin in a random cell"""
        key = self.get_random_cell()
        self.grid[key]["coin"] = True
        return key

    def set_occupied(self, key):
        self.grid[key]["occupied"] = True

    def free_square(self, key):
        self.grid[key]["occupied"] = False

    def reset_visits(self):
        for _, item in self.grid.items():
            item["visited"] = False

    def put_coin_looker(self, key):
        self.grid[key]["coin_looker"] = True
        self.grid[key]["visited"] = True

    def move_coin_looker(self, act):
        key = self.get_coin_looker_pos()
        self.grid[key]["coin_looker"] = False
        self.grid[act]["coin_looker"] = True
        return key

    def remove_coin_looker(self, key):
        self.grid[key]["coin_looker"] = False
        self.free_square(key)

    def get_coin_looker_pos(self):
        for k, v in self.grid.items():
            if v["coin_looker"]:
                return k
        return None
