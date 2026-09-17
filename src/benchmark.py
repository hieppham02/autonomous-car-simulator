"""Đo thuật toán trên cùng một bản đồ, không tính thời gian vẽ/animation."""

from copy import deepcopy
from time import perf_counter

if __package__:
    from .algorithms import a_star, bfs, dijkstra
else:
    from algorithms import a_star, bfs, dijkstra


ALGORITHMS = {"BFS": bfs, "Dijkstra": dijkstra, "A*": a_star}


class BenchmarkRunner:
    """Chạy một lượt đo mỗi frame để cửa sổ vẫn nhận sự kiện."""

    def __init__(self, grid, repetitions=20):
        if not isinstance(repetitions, int) or repetitions < 1:
            raise ValueError("Số lần đo phải là số nguyên dương")
        self.grid = deepcopy(grid)
        self.repetitions = repetitions
        self.results = []
        self.completed_runs = 0
        self.elapsed = 0

    @property
    def done(self):
        return len(self.results) == len(ALGORITHMS)

    @property
    def progress(self):
        return self.completed_runs, self.repetitions * len(ALGORITHMS)

    def step(self):
        if self.done:
            return
        name, algorithm = list(ALGORITHMS.items())[len(self.results)]
        start = perf_counter()
        path, visited = algorithm(self.grid, return_visited=True)
        self.elapsed += perf_counter() - start
        self.completed_runs += 1
        if self.completed_runs % self.repetitions == 0:
            steps = len(path) - 1 if path is not None else None
            self.results.append({
                "algorithm": name,
                "time_ms": self.elapsed * 1000 / self.repetitions,
                "nodes": len(visited),
                "path_length": steps,
                "cost": steps,
                "found": path is not None,
                "repetitions": self.repetitions,
            })
            self.elapsed = 0


def run_benchmark(grid, repetitions=20):
    runner = BenchmarkRunner(grid, repetitions)
    while not runner.done:
        runner.step()
    return runner.results
