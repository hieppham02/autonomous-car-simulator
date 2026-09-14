from collections import deque
from map_model import GridMap


class Node:

    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    # Lấy đường đi sau khi thuật toán đã tìm được node đích
    @staticmethod
    def reconstruct_path(goal_node):
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        path.reverse()
        return path


def bfs(grid):
    start_node = Node(grid.start)

    queue = deque()
    queue.append(start_node)

    visited = set()
    visited.add(grid.start)

    return None


grid = GridMap(5, 5)

grid.start = (0, 0)
grid.goal = (4, 4)

print(bfs(grid))
