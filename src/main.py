import json
import random
from pathlib import Path

import pygame

if __package__:
    from .map_model import GridMap
    from .simulation import Simulation, AnimatedBenchmark
    from .renderer import (
        BACKGROUND, Renderer, configure_layout, create_controls,
        grid_position, layout_size, logical_position, window_viewport,
    )
else:
    from map_model import GridMap
    from simulation import Simulation, AnimatedBenchmark
    from renderer import (
        BACKGROUND, Renderer, configure_layout, create_controls,
        grid_position, layout_size, logical_position, window_viewport,
    )


ROWS = 35
COLUMNS = 50
PATH_STEP_DELAY = 50
SCAN_STEP_DELAY = 15
SCAN_BATCH_SIZE = 1
ENDPOINTS_FILE = Path(__file__).resolve().parent.parent / "data" / "endpoints.json"


def load_endpoints(rows, columns):
    try:
        data = json.loads(ENDPOINTS_FILE.read_text(encoding="utf-8"))
        start = tuple(data["start"])
        goal = tuple(data["goal"])
        valid = lambda point: (
            len(point) == 2
            and 0 <= point[0] < rows
            and 0 <= point[1] < columns
        )
        if valid(start) and valid(goal) and start != goal:
            return start, goal
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return (0, 7), (20, 29)


def save_endpoints(grid):
    ENDPOINTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"start": list(grid.start), "goal": list(grid.goal)}
    ENDPOINTS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def create_demo_map():
    grid = GridMap(ROWS, COLUMNS)
    grid.start, grid.goal = load_endpoints(ROWS, COLUMNS)

    grid.obstacles.update({
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 7),
        (6, 8),
        (6, 9),
    })
    grid.obstacles.discard(grid.start)
    grid.obstacles.discard(grid.goal)

    return grid


def create_grid_map(rows, columns):
    grid = GridMap(rows, columns)
    grid.start = (0, 0)
    grid.goal = (rows - 1, columns - 1)
    return grid


def generate_random_street_map(grid):
    grid.obstacles.clear()
    grid.clear_weights()

    road_rows = {grid.start[0], grid.goal[0]}
    road_columns = {grid.start[1], grid.goal[1]}

    row = random.randint(2, 4)
    while row < grid.rows:
        road_rows.add(row)
        row += random.randint(4, 7)

    column = random.randint(2, 5)
    while column < grid.columns:
        road_columns.add(column)
        column += random.randint(5, 9)

    for row in range(grid.rows):
        for column in range(grid.columns):
            position = (row, column)

            if position in (grid.start, grid.goal):
                continue

            is_road = row in road_rows or column in road_columns

            if not is_road and random.random() < 0.9:
                grid.obstacles.add(position)


def generate_random_sparse_map(grid, density=0.12):
    """Create scattered obstacles while keeping most of the map traversable."""
    grid.obstacles.clear()
    grid.clear_weights()
    for row in range(grid.rows):
        for column in range(grid.columns):
            position = (row, column)
            if position in (grid.start, grid.goal):
                continue
            if random.random() < density:
                grid.obstacles.add(position)


def generate_random_weights(grid, density=0.18):
    """Add weighted terrain without changing the obstacle layout."""
    grid.clear_weights()
    for row in range(grid.rows):
        for column in range(grid.columns):
            position = (row, column)
            if position in (grid.start, grid.goal) or grid.is_obstacle(position):
                continue
            if random.random() < density:
                grid.set_weight(position, random.randint(2, 5))


def edit_obstacle(grid, mouse_position, add_obstacle):
    position = grid_position(mouse_position, grid)
    if position is None or position in (grid.start, grid.goal):
        return False
    was_obstacle = grid.is_obstacle(position)
    if add_obstacle:
        grid.obstacles.add(position)
    else:
        grid.obstacles.discard(position)
    return was_obstacle != add_obstacle


def place_endpoint(grid, mouse_position, endpoint):
    position = grid_position(mouse_position, grid)
    if position is None:
        return False, ""
    other = grid.goal if endpoint == "start" else grid.start
    if position == other:
        return False, "Lỗi: Start và Goal phải khác nhau"
    grid.obstacles.discard(position)
    if endpoint == "start":
        grid.start = position
        return True, f"Đã đặt Start tại {position}"
    grid.goal = position
    return True, f"Đã đặt Goal tại {position}"


class Application:
    def __init__(self):
        self.grid = create_demo_map()
        configure_layout(self.grid)
        self.simulation = Simulation(self.grid)
        self.controls = create_controls()
        self.path_step_delay = PATH_STEP_DELAY
        self.benchmark = None
        self.grid_inputs = {"rows": str(self.grid.rows),
                            "columns": str(self.grid.columns)}
        self.active_input = None
        self.input_select_all = False
        self.grid_message = ""
        self.edit_mode = "obstacle"
        self.random_mode = 0

    def map_changed(self, status):
        self.simulation.reset(self.grid, status)
        # Kết quả/tiến độ đo chỉ có ý nghĩa trên đúng map đã đo.
        self.benchmark = None
        self.edit_mode = "obstacle"

    def create_custom_grid(self):
        try:
            rows = int(self.grid_inputs["rows"])
            columns = int(self.grid_inputs["columns"])
        except ValueError:
            self.grid_message = "Lỗi: chỉ nhập số nguyên"
            return
        if not 5 <= rows <= 50 or not 5 <= columns <= 80:
            self.grid_message = "Lỗi: hàng 5–50, cột 5–80"
            return
        self.grid = create_grid_map(rows, columns)
        configure_layout(self.grid)
        self.controls = create_controls()
        self.grid_inputs = {"rows": str(rows), "columns": str(columns)}
        self.active_input = None
        self.input_select_all = False
        self.grid_message = f"Đã tạo map {rows} × {columns}"
        self.map_changed(self.grid_message)

    def handle_event(self, event, viewport, now):
        if event.type == pygame.KEYDOWN and self.active_input:
            key = "rows" if self.active_input == "rows_input" else "columns"
            if event.key == pygame.K_BACKSPACE:
                self.grid_inputs[key] = (
                    "" if self.input_select_all else self.grid_inputs[key][:-1]
                )
                self.input_select_all = False
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.create_custom_grid()
            elif event.unicode.isdigit() and len(self.grid_inputs[key]) < 3:
                if self.input_select_all:
                    self.grid_inputs[key] = event.unicode
                    self.input_select_all = False
                else:
                    self.grid_inputs[key] += event.unicode
            return
        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            return
        position = logical_position(event.pos, viewport)
        if position is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                action = next((name for name, rect in self.controls.items()
                               if rect.collidepoint(position)), None)
                if action not in ("rows_input", "columns_input"):
                    self.active_input = None
                    self.input_select_all = False
                if action in ("rows_input", "columns_input"):
                    self.active_input = action
                    self.input_select_all = True
                elif action == "apply_grid":
                    self.create_custom_grid()
                elif action == "set_start":
                    self.edit_mode = "start"
                    self.grid_message = "Chọn một ô để đặt Start"
                elif action == "set_goal":
                    self.edit_mode = "goal"
                    self.grid_message = "Chọn một ô để đặt Goal"
                elif action in ("BFS", "Dijkstra", "A*"):
                    self.active_input = None
                    self.input_select_all = False
                    if self.benchmark is not None and not self.benchmark.done:
                        self.benchmark = None
                    self.simulation.start(self.grid, action, now)
                elif action == "benchmark":
                    self.active_input = None
                    self.input_select_all = False
                    if self.benchmark is None or self.benchmark.done:
                        self.benchmark = AnimatedBenchmark(self.grid, self.simulation)
                elif action == "random":
                    self.active_input = None
                    self.input_select_all = False
                    if self.random_mode == 0:
                        generate_random_street_map(self.grid)
                        self.grid_message = "Đã tạo bản đồ đường phố"
                        self.random_mode = 1
                    else:
                        generate_random_sparse_map(self.grid)
                        self.grid_message = "Đã tạo chướng ngại vật mật độ thấp"
                        self.random_mode = 0
                    self.map_changed(self.grid_message)
                elif action == "weights":
                    self.active_input = None
                    self.input_select_all = False
                    generate_random_weights(self.grid)
                    self.map_changed("Đã tạo trọng số ngẫu nhiên")
                elif action == "clear":
                    self.active_input = None
                    self.input_select_all = False
                    self.grid.obstacles.clear()
                    self.grid.clear_weights()
                    self.map_changed("Đã reset vật cản, trọng số và đường đi")
                elif action == "decrease":
                    self.active_input = None
                    self.input_select_all = False
                    self.path_step_delay = max(10, self.path_step_delay - 10)
                elif action == "increase":
                    self.active_input = None
                    self.input_select_all = False
                    self.path_step_delay = min(500, self.path_step_delay + 10)
                elif self.edit_mode in ("start", "goal"):
                    changed, message = place_endpoint(
                        self.grid, position, self.edit_mode,
                    )
                    if message:
                        self.grid_message = message
                    if changed:
                        save_endpoints(self.grid)
                        self.map_changed(message)
                        self.grid_message = message
                elif edit_obstacle(self.grid, position, True):
                    self.active_input = None
                    self.input_select_all = False
                    self.map_changed("Bản đồ đã thay đổi")
            elif event.button == 3 and edit_obstacle(self.grid, position, False):
                self.map_changed("Bản đồ đã thay đổi")
        elif (event.buttons[0] or event.buttons[2]) and self.edit_mode == "obstacle":
            if edit_obstacle(self.grid, position, bool(event.buttons[0])):
                self.map_changed("Bản đồ đã thay đổi")

    def update(self, now):
        if self.benchmark is not None and not self.benchmark.done:
            self.benchmark.update(self.simulation, now, self.path_step_delay,
                                  self.path_step_delay, SCAN_BATCH_SIZE)
        else:
            self.simulation.update(now, self.path_step_delay,
                                   self.path_step_delay, SCAN_BATCH_SIZE)


def main():
    pygame.init()
    app = Application()
    logical_size = layout_size()
    screen = pygame.display.set_mode(logical_size)
    pygame.display.set_caption("Mô phỏng xe tìm đường tự động")
    canvas = pygame.Surface(logical_size)
    renderer = Renderer()
    clock = pygame.time.Clock()
    running = True

    while running:
        viewport = window_viewport(screen.get_size(), logical_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.handle_event(event, viewport, pygame.time.get_ticks())
        if not running:
            break

        app.update(pygame.time.get_ticks())
        renderer.draw(
            canvas, app.grid, app.simulation, app.path_step_delay, app.benchmark,
            app.grid_inputs, app.active_input, app.input_select_all,
            app.grid_message, app.edit_mode,
            logical_position(pygame.mouse.get_pos(), viewport, logical_size),
        )
        screen.fill(BACKGROUND)
        if viewport.size == logical_size:
            screen.blit(canvas, viewport)
        else:
            screen.blit(pygame.transform.smoothscale(canvas, viewport.size), viewport)
        pygame.display.flip()
        clock.tick(144)

    pygame.quit()


if __name__ == "__main__":
    main()
