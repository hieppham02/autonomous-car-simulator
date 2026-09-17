import unittest

from src.algorithms import a_star, bfs, dijkstra
from src.benchmark import run_benchmark
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

    def test_all_algorithms_find_a_shortest_path(self):
        grid = GridMap(5, 5)
        grid.start = (0, 0)
        grid.goal = (0, 4)
        grid.obstacles.update({(0, 1), (0, 2), (0, 3)})

        bfs_path = bfs(grid)
        dijkstra_path = dijkstra(grid)
        a_star_path = a_star(grid)

        self.assertEqual(len(dijkstra_path), len(bfs_path))
        self.assertEqual(len(a_star_path), len(bfs_path))
        self.assertEqual(dijkstra_path[0], grid.start)
        self.assertEqual(dijkstra_path[-1], grid.goal)
        self.assertEqual(a_star_path[0], grid.start)
        self.assertEqual(a_star_path[-1], grid.goal)

    def test_all_algorithms_return_none_when_goal_is_unreachable(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (2, 2)
        grid.obstacles.update({(1, 2), (2, 1)})

        self.assertIsNone(dijkstra(grid))
        self.assertIsNone(a_star(grid))

    def test_weighted_search_costs_are_correct(self):
        grid = GridMap(3, 5)
        grid.start = (1, 0)
        grid.goal = (1, 4)
        for column in (1, 2, 3):
            grid.set_weight((1, column), 5)

        bfs_path = bfs(grid)
        dijkstra_path = dijkstra(grid)
        a_star_path = a_star(grid)

        def cost(path):
            return sum(grid.weight_at(position) for position in path[1:])

        self.assertEqual(len(bfs_path) - 1, 4)
        self.assertEqual(cost(bfs_path), 16)
        self.assertEqual(len(dijkstra_path) - 1, 6)
        self.assertEqual(cost(dijkstra_path), 6)
        self.assertEqual(cost(a_star_path), cost(dijkstra_path))

    def test_algorithms_can_return_search_order_for_animation(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (2, 2)

        for algorithm in (bfs, dijkstra, a_star):
            path, visited_order = algorithm(grid, return_visited=True)

            self.assertEqual(visited_order[0], grid.start)
            self.assertEqual(visited_order[-1], grid.goal)
            self.assertEqual(path[0], grid.start)
            self.assertEqual(path[-1], grid.goal)

    def test_search_details_separate_g_h_and_f(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (2, 2)

        _, _, bfs_details = bfs(grid, return_details=True)
        _, _, a_star_details = a_star(grid, return_details=True)

        self.assertEqual(bfs_details[0]["h"], 0)
        self.assertEqual(bfs_details[0]["f"], 0)
        self.assertEqual(a_star_details[0]["g"], 0)
        self.assertEqual(a_star_details[0]["h"], 4)
        self.assertEqual(a_star_details[0]["f"], 4)

    def test_benchmark_compares_all_algorithms(self):
        grid = GridMap(3, 3)
        grid.start = (0, 0)
        grid.goal = (2, 2)

        results = run_benchmark(grid, repetitions=2)

        self.assertEqual(
            [result["algorithm"] for result in results],
            ["BFS", "Dijkstra", "A*"],
        )
        self.assertTrue(all(result["cost"] == 4 for result in results))


if __name__ == "__main__":
    unittest.main()
