from collections import deque
from heapq import heappop, heappush
from itertools import count

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


def validate_grid(grid):
    if grid.start is None or grid.goal is None:
        raise ValueError("Bản đồ phải có điểm bắt đầu và điểm đích")

    if not grid.is_inside(grid.start) or not grid.is_inside(grid.goal):
        raise ValueError("Điểm bắt đầu hoặc điểm đích nằm ngoài bản đồ")

    if grid.is_obstacle(grid.start) or grid.is_obstacle(grid.goal):
        raise ValueError("Điểm bắt đầu hoặc điểm đích không thể là vật cản")

def build_search_output(
    path,
    visited_order,
    node_details,
    return_visited,
    return_details,
):
    if return_details:
        return path, visited_order, node_details
    if return_visited:
        return path, visited_order
    return path


def bfs(grid, return_visited=False, return_details=False):
    validate_grid(grid)
    start_node = Node(grid.start)

    queue = deque([start_node])
    visited = {grid.start}
    visited_order = []
    node_details = []

    while queue:
        current_node = queue.popleft()
        visited_order.append(current_node.position)
        node_details.append({
            "position": current_node.position,
            "g": current_node.g,
            "h": 0,
            "f": current_node.g,
        })

        if current_node.position == grid.goal:
            path = Node.reconstruct_path(current_node)
            return build_search_output(
                path, visited_order, node_details,
                return_visited, return_details,
            )

        for neighbor_position in grid.get_neighbors(current_node.position):
            if neighbor_position not in visited:
                visited.add(neighbor_position)

                neighbor_node = Node(
                    position=neighbor_position,
                    parent=current_node,
                    g=current_node.g + 1
                )

                queue.append(neighbor_node)

    return build_search_output(
        None, visited_order, node_details,
        return_visited, return_details,
    )


def dijkstra(grid, return_visited=False, return_details=False):
    validate_grid(grid)

    start_node = Node(grid.start)
    priority_queue = []
    insertion_order = count()
    best_cost = {grid.start: 0}
    visited_order = []
    node_details = []

    heappush(priority_queue, (0, next(insertion_order), start_node))

    while priority_queue:
        current_cost, _, current_node = heappop(priority_queue)

        if current_cost != best_cost[current_node.position]:
            continue

        visited_order.append(current_node.position)
        node_details.append({
            "position": current_node.position,
            "g": current_node.g,
            "h": 0,
            "f": current_node.g,
        })

        if current_node.position == grid.goal:
            path = Node.reconstruct_path(current_node)
            return build_search_output(
                path, visited_order, node_details,
                return_visited, return_details,
            )

        for neighbor_position in grid.get_neighbors(current_node.position):
            new_cost = current_node.g + grid.weight_at(neighbor_position)

            if new_cost < best_cost.get(neighbor_position, float("inf")):
                best_cost[neighbor_position] = new_cost
                neighbor_node = Node(
                    position=neighbor_position,
                    parent=current_node,
                    g=new_cost,
                )
                heappush(
                    priority_queue,
                    (neighbor_node.g, next(insertion_order), neighbor_node),
                )

    return build_search_output(
        None, visited_order, node_details,
        return_visited, return_details,
    )


def manhattan_distance(position, goal):
    row, column = position
    goal_row, goal_column = goal
    return abs(row - goal_row) + abs(column - goal_column)


def a_star(grid, return_visited=False, return_details=False):
    validate_grid(grid)

    start_h = manhattan_distance(grid.start, grid.goal)
    start_node = Node(grid.start, h=start_h)
    priority_queue = []
    insertion_order = count()
    best_cost = {grid.start: 0}
    visited_order = []
    node_details = []

    heappush(
        priority_queue,
        (start_node.f, next(insertion_order), start_node),
    )

    while priority_queue:
        _, _, current_node = heappop(priority_queue)

        if current_node.g != best_cost[current_node.position]:
            continue

        visited_order.append(current_node.position)
        node_details.append({
            "position": current_node.position,
            "g": current_node.g,
            "h": current_node.h,
            "f": current_node.f,
        })

        if current_node.position == grid.goal:
            path = Node.reconstruct_path(current_node)
            return build_search_output(
                path, visited_order, node_details,
                return_visited, return_details,
            )

        for neighbor_position in grid.get_neighbors(current_node.position):
            new_cost = current_node.g + grid.weight_at(neighbor_position)

            if new_cost < best_cost.get(neighbor_position, float("inf")):
                best_cost[neighbor_position] = new_cost
                neighbor_node = Node(
                    position=neighbor_position,
                    parent=current_node,
                    g=new_cost,
                    h=manhattan_distance(neighbor_position, grid.goal),
                )
                heappush(
                    priority_queue,
                    (neighbor_node.f, next(insertion_order), neighbor_node),
                )

    return build_search_output(
        None, visited_order, node_details,
        return_visited, return_details,
    )
