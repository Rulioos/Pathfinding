from grid import State
from copy import deepcopy
import time
from search import *


class Board:
    def __init__(self, win_width, win_height, square_size=20):
        self.state = State(win_width, win_height, square_size)
        self.goal = self.state.put_coin()
        self.state.put_coin_looker(self.state.get_random_cell())
        self.movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.movements = [tuple(p * q for p, q in zip((square_size, square_size), item)) for item in
                          self.movements]

    def new_goal(self):
        self.state.grid[self.goal]["coin"] = False
        self.goal = self.state.put_coin()

    def goal_test(self, state):
        """Checks if the coin looker is on the same square as the coin"""
        if self.goal == state.get_coin_looker_pos():
            self.state.reset_visits()
            return True
        else:
            return False

    def path_cost(self, c, next_state):
        distance = heuristic_euclidean(self.goal, next_state.get_coin_looker_pos())
        return c + distance

    def get_successor(self, state):
        """Get the child of the current position of the coin_looker"""
        w = state.width
        h = state.height
        sz = state.square_size
        (x, y) = state.get_coin_looker_pos()
        possible_next_positions = [tuple(p + q for p, q in zip((x, y), item)) for item in self.movements]

        successors = []
        for i, coord in enumerate(possible_next_positions):
            if coord in state.grid.keys() and not state.grid[coord]["occupied"] and not state.grid[coord]["visited"]:
                act = self.movements[i]

                st = state.__copy__()
                # st.width, st.height, st.square_size = w, h, sz
                # st.grid = deepcopy(state.grid)
                st.put_coin_looker(coord)
                st.remove_coin_looker((x, y))
                successors.append((act, st))

        return successors

#
# b = Board(100, 100)
# start_time = time.perf_counter()
# node, n = dfs_tree_search(b)
# end_time = time.perf_counter()
# print(end_time - start_time)
#
# path = node.path()
# path.reverse()
#
# print("goal:", b.goal)
# for item in path:
#     print(item.action)
#     print(item.state.get_coin_looker_pos())
#     print("____________")
