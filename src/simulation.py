"""Trạng thái quét và di chuyển; độc lập với phần vẽ Pygame."""

from time import perf_counter

if __package__:
    from .benchmark import ALGORITHMS, BenchmarkRunner
else:
    from benchmark import ALGORITHMS, BenchmarkRunner


class Simulation:
    def __init__(self, grid):
        self.reset(grid)

    def reset(self, grid, status="Chọn thuật toán để bắt đầu"):
        self.algorithm = None
        self.status = status
        self.phase = "idle"
        self.path = []
        self.visited = []
        self.details = []
        self.scanned_cells = set()
        self.visible_path = set()
        self.scan_index = 0
        self.path_index = 0
        self.car_position = grid.start
        self.direction = (-1, 0)
        self.metrics = None
        self.time_ms = None
        self.last_step = 0

    def start(self, grid, algorithm, now):
        self.reset(grid)
        self.algorithm = algorithm
        start = perf_counter()
        path, self.visited, self.details = ALGORITHMS[algorithm](
            grid, return_details=True,
        )
        self.time_ms = (perf_counter() - start) * 1000
        self.path = path if path is not None else []
        self.phase = "scanning"
        self.status = "Đang quét tìm đường"
        self.last_step = now

    def update(self, now, delay, scan_delay=15, scan_batch=4):
        if self.phase == "scanning" and now - self.last_step >= scan_delay:
            end = min(self.scan_index + scan_batch, len(self.visited))
            self.scanned_cells.update(self.visited[self.scan_index:end])
            self.scan_index = end
            if end:
                self.metrics = self.details[end - 1]
            self.last_step = now
            if end == len(self.visited):
                self.phase = "moving" if self.path else "done"
                self.status = "Xe đang di chuyển" if self.path else "Không tìm thấy đường"
        elif self.phase == "moving" and now - self.last_step >= delay:
            position = self.path[self.path_index]
            if position != self.car_position:
                self.direction = (
                    position[0] - self.car_position[0],
                    position[1] - self.car_position[1],
                )
            self.car_position = position
            self.visible_path.add(position)
            self.path_index += 1
            self.last_step = now
            if self.path_index == len(self.path):
                self.phase = "done"
                self.status = "Đã đến đích"

    @property
    def result_visible(self):
        return self.phase in ("moving", "done")

    @property
    def cost(self):
        return len(self.path) - 1 if self.path else None


class AnimatedBenchmark:
    """Chỉ công bố bảng sau khi đo và mô phỏng đủ cả ba thuật toán."""

    def __init__(self, grid, simulation, repetitions=20):
        self.runner = BenchmarkRunner(grid, repetitions)
        self.completed = 0
        self.names = list(ALGORITHMS)
        simulation.reset(grid)

    @property
    def done(self):
        return self.completed == len(self.names) and self.runner.done

    @property
    def results(self):
        return self.runner.results if self.done else []

    @property
    def repetitions(self):
        return self.runner.repetitions

    @property
    def progress(self):
        return self.completed, len(self.names)

    def update(self, simulation, now, delay, scan_delay, scan_batch):
        self.runner.step()
        if self.completed == len(self.names):
            return
        if simulation.phase == "idle":
            simulation.start(self.runner.grid, self.names[self.completed], now)
        elif simulation.phase == "done":
            self.completed += 1
            if self.completed < len(self.names):
                simulation.reset(self.runner.grid)
        else:
            simulation.update(now, delay, scan_delay, scan_batch)
