import unittest

from src.algorithms import a_star, bfs, dijkstra
from src.map_model import GridMap


class BFSTests(unittest.TestCase):
    def test_bfs_finds_a_shortest_path(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (0, 2)
        grid.obstacles.add((0, 1))

        path = bfs(grid)

        self.assertEqual(path[0], grid.start)
        self.assertEqual(path[-1], grid.goal)
        self.assertEqual(len(path) - 1, 4)

    def test_bfs_returns_none_when_goal_is_unreachable(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (2, 2)
        grid.obstacles.update({(1, 2), (2, 1)})

        self.assertIsNone(bfs(grid))

    def test_future_algorithms_are_placeholders(self):
        grid = GridMap(2, 2)

        with self.assertRaises(NotImplementedError):
            dijkstra(grid)

        with self.assertRaises(NotImplementedError):
            a_star(grid)


if __name__ == "__main__":
    unittest.main()
