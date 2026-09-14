from collections import deque


class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

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

    queue = deque([start_node])
    visited = {grid.start}

    while queue:
        current_node = queue.popleft()

        if current_node.position == grid.goal:
            return Node.reconstruct_path(current_node)

        for neighbor_position in grid.get_neighbors(current_node.position):
            if neighbor_position not in visited:
                visited.add(neighbor_position)

                neighbor_node = Node(
                    position=neighbor_position,
                    parent=current_node,
                    g=current_node.g + 1
                )

                queue.append(neighbor_node)

    return None
