from src.utils import *
from math import sqrt, pow


class Node:
    """ A node used in tree search """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def path(self):
        """Returns the path to the first parent node"""
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    def expand(self, board):
        """Yield this node successors"""
        for (action, next_state) in board.get_successor(self.state):
            yield Node(next_state, self, action,
                       board.path_cost(self.path_cost, next_state))


def tree_search(board, fringe):
    fringe.append(Node(board.state))
    n = 0
    while fringe:
        node = fringe.pop()
        n += 1
        if board.goal_test(node.state):
            return node, n
        fringe.extend(node.expand(board))
    return None, n


def bfs_tree_search(board):
    return tree_search(board, FIFOQueue())


def heuristic_euclidean(s1, s2):
    return sqrt(pow(s1[0] - s2[0], 2) + pow(s1[1] - s2[1], 2))


def heuristic_manhattan(s1, s2):
    return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])


def a_star_search(board):
    return tree_search(board, PriorityQueue(f=lambda n: board.path_cost(n.path_cost, n.state)))
