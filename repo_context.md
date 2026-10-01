

# FILE: data/endpoints.json

{
  "start": [
    10,
    3
  ],
  "goal": [
    20,
    40
  ]
}

# FILE: docs/00-scope.md

# Đặc tả phạm vi bước 1

## Mục tiêu

Xây dựng nền tảng cho chương trình mô phỏng xe tự động đi từ điểm xuất phát đến đích trong bản đồ dạng lưới có vật cản và các mức chi phí di chuyển khác nhau.

## Mô hình bài toán

- Trạng thái cơ bản: tọa độ ô `(x, y)`.
- Hành động: đi lên, xuống, trái, phải.
- Ô vật cản: không thể đi vào.
- Cạnh: một bước di chuyển giữa hai ô kề nhau.
- Chi phí cạnh: chi phí của ô đích; mọi chi phí phải không âm.
- Mục tiêu: đạt ô đích với đường hợp lệ.

## Ranh giới

Phiên bản đầu mô phỏng lập kế hoạch đường đi trên bản đồ đã biết. Không mô phỏng camera, nhận dạng vật thể, động lực học xe, điều khiển vô-lăng liên tục hoặc giao thông nhiều xe.

## Tiêu chí đầu ra

Mỗi lần chạy cần có đường đi hoặc trạng thái không tìm thấy đường, số bước, tổng chi phí, số nút đã mở rộng và thời gian tìm kiếm.


# FILE: docs/01-architecture.md

# Kiến trúc dự kiến

## Các thành phần

1. **Map model**: đã triển khai trong `src/map_model.py`; quản lý lưới, vật cản, chi phí, điểm đầu, điểm đích và láng giềng 4 hướng.
2. **Search algorithms**: giao diện chung cho BFS, Dijkstra và A*.
3. **Simulation**: xe thực hiện từng bước theo đường đi, dừng khi lỗi hoặc đến đích.
4. **Renderer/UI**: vẽ bản đồ, trạng thái tìm kiếm, xe và bảng điều khiển.
5. **Experiment runner**: chạy cùng một cấu hình cho nhiều thuật toán và ghi số liệu.
6. **Persistence**: lưu và tải bản đồ, cấu hình thực nghiệm.

## Nguyên tắc kết nối

- Thuật toán không phụ thuộc giao diện.
- Giao diện chỉ tiêu thụ trạng thái và kết quả tìm kiếm.
- Cùng một bản đồ, điểm đầu, điểm đích, thứ tự xét hàng xóm và quy tắc chi phí được dùng khi so sánh.
- Hoạt ảnh không được tính vào thời gian chạy thuật toán.

## Công nghệ dự kiến

Python và Pygame cho bản thử nghiệm trực quan. Có thể thay đổi nếu giảng viên yêu cầu nền tảng khác.


# FILE: docs/02-algorithms.md

# Đặc tả thuật toán

## BFS

Hàng đợi FIFO, ưu tiên độ sâu nhỏ nhất. Tối ưu số bước khi mọi cạnh có cùng chi phí; không tối ưu tổng chi phí trong bản đồ có trọng số khác nhau.

## Dijkstra

Hàng đợi ưu tiên theo chi phí tích lũy `g(n)`. Tối ưu tổng chi phí khi chi phí cạnh không âm.

## A*

Hàng đợi ưu tiên theo `f(n) = g(n) + h(n)`. Với lưới 4 hướng, heuristic mặc định là khoảng cách Manhattan nhân chi phí bước nhỏ nhất. Heuristic phải không vượt chi phí thật.

## Kết quả chung

Mỗi thuật toán trả về đường đi, chi phí, số bước, số nút mở rộng, trạng thái thành công/thất bại và nhật ký các nút đã xét để trực quan hóa.


# FILE: docs/03-experiments.md

# Kế hoạch thực nghiệm

1. Bản đồ thông thoáng, chi phí đồng đều.
2. Mê cung nhiều vật cản và ngõ cụt.
3. Tuyến ít bước nhưng chi phí cao so với tuyến vòng có chi phí thấp.
4. Đích bị bao kín, không tồn tại đường đi.
5. Kích thước bản đồ tăng dần: 20x20, 50x50, 100x100.
6. Mở rộng: thêm vật cản khi xe đang chạy và lập kế hoạch lại.

Các chỉ số: thời gian tìm đường, số nút mở rộng, số bước, tổng chi phí và bộ nhớ sử dụng nếu đo được.


# FILE: docs/04-roadmap.md

# Lộ trình

## Bước 1 — Khởi tạo (hiện tại)

- Chốt phạm vi, mô hình dữ liệu và kiến trúc thư mục.
- Đã tạo các tệp khung cho mô hình bản đồ và các thành phần liên quan; chưa có mã triển khai.

## Bước 2 — Mô hình và thuật toán

- Định nghĩa bản đồ, trạng thái, kết quả tìm kiếm.
- Cài đặt và kiểm tra riêng BFS, Dijkstra, A*.

## Bước 3 — Giao diện mô phỏng

- Vẽ lưới, vật cản, chi phí, trạng thái tìm kiếm và xe.
- Thêm điều khiển chạy/tạm dừng/chạy từng bước.

## Bước 4 — Đánh giá và hoàn thiện

- Chạy bộ kịch bản thực nghiệm.
- Xuất số liệu, viết báo cáo và chuẩn bị demo.


# FILE: README.md

# Mô phỏng điều khiển xe tự động bằng BFS, Dijkstra và A*

Bài tập lớn môn Trí tuệ nhân tạo: mô phỏng xe di chuyển trên bản đồ dạng lưới, lập kế hoạch đường đi bằng BFS, Dijkstra hoặc A*, sau đó trực quan hóa và so sánh kết quả.

## Trạng thái

Đã có mô phỏng Pygame với BFS, Dijkstra và A*: quét node, tìm đường rồi cho xe di chuyển. Giao diện gồm panel điều khiển bên trái, bản đồ ở giữa và kết quả/benchmark bên phải.

## Chạy và sử dụng

```powershell
py src/main.py
```

- Bấm BFS, Dijkstra hoặc A* để chạy lại mô phỏng từ điểm đầu.
- Giao diện dùng light theme; panel trái thu gọn, bản đồ ở giữa và kết quả/benchmark ở panel phải.
- Nhập số hàng (5–50) và số cột (5–80), sau đó bấm `Tạo grid map` hoặc Enter. Khi nhấp vào ô nhập, giá trị cũ được chọn toàn bộ để số mới thay thế ngay; sau khi nhập có con trỏ nhấp nháy. Map mới đặt start ở góc trên trái và goal ở góc dưới phải; cell luôn giữ hình vuông. Panel giữa tự lấy kích thước grid cộng 10 px đệm mỗi cạnh nên không còn khoảng trống bên trong panel.
- Bấm `Đặt Start` hoặc `Đặt Goal`, sau đó chọn một ô trên grid. Điểm mới không thể trùng điểm còn lại; obstacle tại ô được chọn sẽ tự xóa.
- `Reset bản đồ` chỉ xóa obstacle, đường quét và animation; vị trí Start và Goal được giữ nguyên.
- Giữ chuột trái để tô vật cản, chuột phải để xóa. Start và goal được bảo vệ.
- Quét node màu xanh nhạt, đường xe đã đi màu vàng, obstacle liền khối màu đen.
- Xe dùng ảnh `assets/car-topdown.png`, xoay theo hướng di chuyển.
- Nút `− / ms / +` chỉnh thời gian mỗi bước trong khoảng 10–500 ms, bước điều chỉnh 10 ms.
- Benchmark lần lượt mô phỏng BFS → Dijkstra → A*: về trạng thái chờ, quét node rồi cho xe di chuyển. Chỉ khi cả ba lượt mô phỏng hoàn tất mới hiện bảng so sánh; lượt không có đường kết thúc sau khi quét.
- Benchmark đo trên bản sao của map hiện tại, mỗi thuật toán 20 lượt. Bảng hiển thị thời gian trung bình (ms), số node được xét (bao gồm start/goal khi tới đích), số bước và chi phí. Thời gian đo không tính vẽ giao diện hoặc chờ animation.
- Bản đồ hiện không có trọng số: chi phí bằng số bước; không có đường được hiển thị bằng `—`.
- Thay đổi map sẽ hủy animation, hủy benchmark đang chạy và xóa kết quả cũ. Chọn riêng một thuật toán cũng hủy benchmark đang chạy. Bấm benchmark lần nữa sau khi hoàn tất để đo và mô phỏng lại.
- Có thể thay đổi kích thước cửa sổ; giao diện và vị trí chuột được quy đổi theo cùng tỉ lệ.

Kiểm tra tự động (bao gồm Pygame headless):

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```

## Cấu trúc chương trình

- `docs/`: đặc tả bài toán, kiến trúc và kế hoạch thực hiện.
- `src/main.py`: xử lý sự kiện và vòng lặp ứng dụng.
- `src/renderer.py`: bố cục, vẽ bản đồ, xe và bảng kết quả.
- `src/simulation.py`: quản lý pha quét và di chuyển.
- `src/benchmark.py`: đo ba thuật toán, mỗi frame một lượt đo.
- `src/algorithms.py`, `src/map_model.py`: thuật toán và dữ liệu lưới.
- `assets/`: ảnh xe.
- `data/maps/`: bản đồ mẫu và bản đồ thực nghiệm.
- `tests/`: kiểm thử thuật toán và mô phỏng.
- `reports/`: kết quả đo và tài liệu báo cáo.

## Phạm vi chương trình

- Bản đồ ô vuông 2D, di chuyển 4 hướng.
- Vật cản; mỗi bước di chuyển có chi phí bằng 1.
- Ba thuật toán: BFS, Dijkstra, A*.
- Xe chạy theo đường đã tìm; phần nhận diện cảm biến/vật lý thực không thuộc phiên bản đầu.
- 
## Thư viện và cài đặt môi trường

Dự án sử dụng Python 3.11 trở lên và Pygame để tạo cửa sổ mô phỏng, vẽ bản đồ, nhận thao tác chuột/bàn phím và chạy hoạt ảnh. Các thuật toán BFS, Dijkstra và A* sẽ dùng thư viện chuẩn của Python, nên chưa cần thêm gói bên ngoài.

Danh sách thư viện được lưu trong `requirements.txt`. Cài đặt bằng:

```powershell
py -m pip install -r requirements.txt
```

Kiểm tra Pygame sau khi cài đặt:

```powershell
py -c "import pygame; print(pygame.version.ver)"
```


# FILE: repo_context.md



# FILE: requirements.txt

pygame==2.6.1


# FILE: run.py

from src.main import main


if __name__ == "__main__":
    main()


# FILE: src/algorithms.py

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


# FILE: src/benchmark.py

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
            cost = (
                sum(self.grid.weight_at(position) for position in path[1:])
                if path is not None else None
            )
            self.results.append({
                "algorithm": name,
                "time_ms": self.elapsed * 1000 / self.repetitions,
                "nodes": len(visited),
                "path_length": steps,
                "cost": cost,
                "found": path is not None,
                "repetitions": self.repetitions,
            })
            self.elapsed = 0


def run_benchmark(grid, repetitions=20):
    runner = BenchmarkRunner(grid, repetitions)
    while not runner.done:
        runner.step()
    return runner.results


# FILE: src/main.py

import json
import random
import sys
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

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


# FILE: src/map_model.py

import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


class GridMap:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.start = None
        self.goal = None
        self.obstacles = set()
        self.weights = {}

    # Kiểm tra xem một vị trí có nằm trong bản đồ hay không
    def is_inside(self, position):
        row, column = position
        return (
            0 <= row < self.rows
            and 0 <= column < self.columns
        )

    # Kiểm tra xem một vị trí có phải là vật cản hay không
    def is_obstacle(self, position):
        return position in self.obstacles

    def weight_at(self, position):
        """Return traversal cost for a cell; normal cells cost one."""
        return max(1, self.weights.get(position, 1))

    def set_weight(self, position, weight):
        if not self.is_inside(position) or position in self.obstacles:
            return
        weight = max(1, int(weight))
        if weight == 1:
            self.weights.pop(position, None)
        else:
            self.weights[position] = weight

    def clear_weights(self):
        self.weights.clear()

    # Lấy các ô hàng xóm có thể đi đến theo 4 hướng
    def get_neighbors(self, position):
        row, column = position
        directions = [
            (-1, 0),  # Lên
            (1, 0),   # Xuống
            (0, -1),  # Trái
            (0, 1)    # Phải
        ]
        neighbors = []
        for delta_row, delta_column in directions:
            next_position = (
                row + delta_row,
                column + delta_column
            )
            if (
                self.is_inside(next_position)
                and not self.is_obstacle(next_position)
            ):
                neighbors.append(next_position)

        return neighbors


# FILE: src/renderer.py

"""Light-theme layout and rendering for the Pygame application."""

from pathlib import Path

import pygame


WIDTH, HEIGHT = 1600, 700
MARGIN = 16
GAP = 14
HEADER_HEIGHT = 0
CONTENT_TOP = MARGIN

LEFT_X, LEFT_WIDTH = MARGIN, 210
CENTER_X, CENTER_WIDTH = LEFT_X + LEFT_WIDTH + GAP, 940
RIGHT_X = CENTER_X + CENTER_WIDTH + GAP
RIGHT_WIDTH = WIDTH - RIGHT_X - MARGIN

GRID_AREA = pygame.Rect(
    CENTER_X + 14,
    CONTENT_TOP + 14,
    CENTER_WIDTH - 28,
    HEIGHT - CONTENT_TOP - MARGIN - 28,
)


def configure_layout(grid):
    """Keep one fixed logical viewport for every grid size."""
    global WIDTH, HEIGHT, CENTER_WIDTH, RIGHT_X, RIGHT_WIDTH
    WIDTH, HEIGHT = 1600, 700
    CENTER_WIDTH = 940
    RIGHT_X = CENTER_X + CENTER_WIDTH + GAP
    RIGHT_WIDTH = WIDTH - RIGHT_X - MARGIN
    GRID_AREA.update(
        CENTER_X + 14,
        CONTENT_TOP + 14,
        CENTER_WIDTH - 28,
        HEIGHT - CONTENT_TOP - MARGIN - 28,
    )
    return WIDTH, HEIGHT


def layout_size():
    return WIDTH, HEIGHT

BACKGROUND = (238, 243, 248)       # #EEF3F8
CARD = (255, 255, 255)
CARD_BORDER = (203, 214, 226)      # #CBD6E2
TEXT = (31, 45, 61)                # #1F2D3D
MUTED = (104, 122, 145)
SECONDARY_TEXT = (92, 111, 134)
PRIMARY = (47, 128, 237)           # #2F80ED
PRIMARY_HOVER = (70, 146, 242)     # #4692F2
SECONDARY_BUTTON = (231, 238, 247) # #E7EEF7
SECONDARY_HOVER = (216, 228, 242)
DANGER = (217, 65, 78)             # #D9414E
DANGER_HOVER = (229, 82, 94)
DISABLED = (222, 229, 237)
INSET = (246, 248, 251)
ROW_SELECTED = (232, 242, 255)
WEIGHT_COLORS = {
    2: (255, 245, 190),
    3: (255, 225, 160),
    4: (255, 200, 150),
    5: (255, 175, 150),
}
WHITE = (255, 255, 255)

GRID_LINE = (184, 196, 211)
GREEN = (35, 190, 92)
RED = (224, 61, 72)
BLACK = (55, 59, 66)
YELLOW = (255, 211, 45)
SCANNED_BLUE = (181, 220, 249)
BLUE_DARK = (31, 102, 190)


def set_font(size, bold=False):
    path = pygame.font.match_font(["segoeui", "arial", "dejavusans"])
    font = pygame.font.Font(path, size)
    font.set_bold(bold)
    return font


def create_controls():
    x = LEFT_X + 16
    width = LEFT_WIDTH - 32
    return {
        "BFS": pygame.Rect(x, CONTENT_TOP + 48, width, 36),
        "Dijkstra": pygame.Rect(x, CONTENT_TOP + 92, width, 36),
        "A*": pygame.Rect(x, CONTENT_TOP + 136, width, 36),
        "benchmark": pygame.Rect(x, CONTENT_TOP + 244, width, 38),
        # Kept for backward-compatible event handling; these controls are
        # intentionally not rendered because the application uses a fixed map.
        "rows_input": pygame.Rect(CENTER_X - 20, CONTENT_TOP + 341, 16, 32),
        "columns_input": pygame.Rect(CENTER_X - 20, CONTENT_TOP + 381, 16, 32),
        "apply_grid": pygame.Rect(CENTER_X - 20, CONTENT_TOP + 424, 16, 36),
        "set_start": pygame.Rect(x, CONTENT_TOP + 362, 84, 36),
        "set_goal": pygame.Rect(x + 94, CONTENT_TOP + 362, 84, 36),
        "random": pygame.Rect(x, CONTENT_TOP + 406, width, 36),
        "weights": pygame.Rect(x, CONTENT_TOP + 450, width, 36),
        "clear": pygame.Rect(x, CONTENT_TOP + 494, width, 36),
        "decrease": pygame.Rect(x, CONTENT_TOP + 618, 36, 34),
        "increase": pygame.Rect(x + width - 36, CONTENT_TOP + 618, 36, 34),
    }


def grid_geometry(grid):
    cell = max(1.0, min(
        GRID_AREA.width / grid.columns,
        GRID_AREA.height / grid.rows,
    ))
    width = round(cell * grid.columns)
    height = round(cell * grid.rows)
    return cell, cell, pygame.Rect(
        GRID_AREA.centerx - width // 2,
        GRID_AREA.centery - height // 2,
        width,
        height,
    )


def grid_panel_geometry(grid):
    return pygame.Rect(CENTER_X, CONTENT_TOP, CENTER_WIDTH,
                       HEIGHT - CONTENT_TOP - MARGIN)


def grid_position(mouse_position, grid):
    cell_width, cell_height, rect = grid_geometry(grid)
    if not rect.collidepoint(mouse_position):
        return None
    row = int((mouse_position[1] - rect.y) / cell_height)
    column = int((mouse_position[0] - rect.x) / cell_width)
    position = (row, column)
    return position if grid.is_inside(position) else None


def window_viewport(size, logical_size=None):
    logical_width, logical_height = logical_size or layout_size()
    scale = min(size[0] / logical_width, size[1] / logical_height)
    rect = pygame.Rect(0, 0, max(1, int(logical_width * scale)),
                       max(1, int(logical_height * scale)))
    rect.center = (size[0] // 2, size[1] // 2)
    return rect


def logical_position(position, viewport, logical_size=None):
    if not viewport.collidepoint(position):
        return None
    logical_width, logical_height = logical_size or layout_size()
    return (
        (position[0] - viewport.x) * logical_width // viewport.width,
        (position[1] - viewport.y) * logical_height // viewport.height,
    )


class Renderer:
    def __init__(self):
        self.app_title = set_font(25, True)
        self.panel_title = set_font(18, True)
        self.button_font = set_font(15)
        self.button_bold = set_font(15, True)
        self.body = set_font(15)
        self.secondary = set_font(13)
        self.stat = set_font(15, True)
        self.weight_font = set_font(10, True)
        self.weight_labels = {
            value: self.weight_font.render(str(value), True, TEXT)
            for value in range(2, 6)
        }

        path = Path(__file__).resolve().parent.parent / "assets" / "car-topdown.png"
        source = pygame.image.load(str(path)).convert_alpha()
        self.car_source = source.subsurface(source.get_bounding_rect()).copy()
        self.car_icon = pygame.transform.smoothscale(self.car_source, (18, 40))
        flag_path = Path(__file__).resolve().parent.parent / "assets" / "finish-flag.png"
        flag_source = pygame.image.load(str(flag_path)).convert_alpha()
        self.flag_source = flag_source.subsurface(flag_source.get_bounding_rect()).copy()
        self.car_cache = {}
        self.controls = create_controls()
        self.mouse_position = (-1, -1)

    def car_images(self, cell):
        if cell not in self.car_cache:
            scale = max(2, cell - 2) / max(self.car_source.get_size())
            base = pygame.transform.smoothscale(
                self.car_source,
                (max(1, round(self.car_source.get_width() * scale)),
                 max(1, round(self.car_source.get_height() * scale))),
            )
            self.car_cache[cell] = {
                (-1, 0): base,
                (1, 0): pygame.transform.rotate(base, 180),
                (0, -1): pygame.transform.rotate(base, 90),
                (0, 1): pygame.transform.rotate(base, -90),
            }
        return self.car_cache[cell]

    def draw_text(self, screen, text, position, color=TEXT, font=None):
        screen.blit((font or self.body).render(str(text), True, color), position)

    def draw_card(self, screen, rect, title=None):
        rect = pygame.Rect(rect)
        pygame.draw.rect(screen, CARD, rect, border_radius=11)
        pygame.draw.rect(screen, CARD_BORDER, rect, 1, border_radius=11)
        if title:
            self.draw_text(screen, title, (rect.x + 16, rect.y + 14),
                           font=self.panel_title)
        return rect

    def draw_button(self, screen, key, label, style="secondary",
                    selected=False, disabled=False):
        rect = self.controls[key]
        hovered = rect.collidepoint(self.mouse_position) and not disabled
        if disabled:
            color, text_color = DISABLED, MUTED
        elif selected or style == "primary":
            color = PRIMARY_HOVER if hovered else PRIMARY
            text_color = WHITE
        elif style == "danger":
            color = DANGER_HOVER if hovered else DANGER
            text_color = WHITE
        else:
            color = SECONDARY_HOVER if hovered else SECONDARY_BUTTON
            text_color = TEXT

        pygame.draw.rect(screen, color, rect, border_radius=7)
        pygame.draw.rect(screen, CARD_BORDER, rect, 1, border_radius=7)
        font = self.button_bold if selected or style == "primary" else self.button_font
        rendered = font.render(label, True, text_color)
        screen.blit(rendered, rendered.get_rect(center=rect.center))

    def draw_input(self, screen, key, value, active, select_all=False):
        rect = self.controls[key]
        pygame.draw.rect(screen, WHITE if active else INSET, rect, border_radius=6)
        pygame.draw.rect(screen, PRIMARY if active else CARD_BORDER, rect,
                         2 if active else 1, border_radius=6)
        rendered = self.body.render(value, True, TEXT)
        text_rect = rendered.get_rect(center=rect.center)
        if active and select_all and value:
            pygame.draw.rect(screen, (193, 220, 255),
                             text_rect.inflate(8, 4), border_radius=3)
        screen.blit(rendered, text_rect)
        if active and not select_all and pygame.time.get_ticks() % 1000 < 500:
            caret_x = min(rect.right - 7, text_rect.right + 2)
            pygame.draw.line(screen, PRIMARY, (caret_x, rect.y + 7),
                             (caret_x, rect.bottom - 7), 2)

    def draw_label_value(self, screen, label, value, y):
        self.draw_text(screen, label, (RIGHT_X + 18, y), SECONDARY_TEXT)
        rendered = self.body.render(str(value), True, TEXT)
        screen.blit(rendered, rendered.get_rect(
            midright=(RIGHT_X + RIGHT_WIDTH - 18, y + 9)
        ))

    def draw_header(self, screen):
        self.draw_text(screen, "Mô phỏng xe tìm đường tự động",
                       (MARGIN + 2, MARGIN - 2), font=self.app_title)
        self.draw_text(screen, "BFS  •  Dijkstra  •  A*",
                       (MARGIN + 3, MARGIN + 29), MUTED, self.secondary)

    def draw_grid(self, screen, grid, simulation):
        cell_width, cell_height, rect = grid_geometry(grid)
        pygame.draw.rect(screen, WHITE, rect)
        for row in range(grid.rows):
            for column in range(grid.columns):
                position = (row, column)
                x1 = rect.x + round(column * cell_width)
                y1 = rect.y + round(row * cell_height)
                x2 = rect.x + round((column + 1) * cell_width)
                y2 = rect.y + round((row + 1) * cell_height)
                cell_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
                weight = grid.weight_at(position)
                is_obstacle = grid.is_obstacle(position)
                color = WEIGHT_COLORS.get(weight, WHITE)
                if position == grid.start:
                    color = GREEN
                elif position == grid.goal:
                    color = WHITE
                elif is_obstacle:
                    color = BLACK
                elif position in simulation.visible_path:
                    color = YELLOW
                elif position in simulation.scanned_cells:
                    color = SCANNED_BLUE
                pygame.draw.rect(screen, color, cell_rect)
                if (not is_obstacle
                        and min(cell_width, cell_height) >= 3):
                    pygame.draw.rect(screen, GRID_LINE, cell_rect, 1)
                if position == grid.goal:
                    flag_size = max(2, round(min(cell_width, cell_height) - 2))
                    flag = pygame.transform.smoothscale(
                        self.flag_source, (flag_size, flag_size)
                    )
                    screen.blit(flag, flag.get_rect(center=cell_rect.center))
                elif (weight > 1
                      and not is_obstacle
                      and min(cell_width, cell_height) >= 10):
                    label = self.weight_labels.get(weight)
                    if label is None:
                        label = self.weight_font.render(str(weight), True, TEXT)
                    screen.blit(label, label.get_rect(center=cell_rect.center))

        if simulation.car_position is not None:
            row, column = simulation.car_position
            center = (
                round(rect.x + (column + 0.5) * cell_width),
                round(rect.y + (row + 0.5) * cell_height),
            )
            car = self.car_images(
                max(2, round(min(cell_width, cell_height)))
            )[simulation.direction]
            screen.blit(car, car.get_rect(center=center))
        pygame.draw.rect(screen, CARD_BORDER, rect, 1)

    def draw_map_card(self, screen, grid, simulation):
        self.draw_card(screen, grid_panel_geometry(grid))
        self.draw_grid(screen, grid, simulation)

    def draw_algorithm_card(self, screen, simulation):
        self.draw_card(screen, (LEFT_X, CONTENT_TOP, LEFT_WIDTH, 190), "Thuật toán")
        for name in ("BFS", "Dijkstra", "A*"):
            self.draw_button(screen, name, name,
                             selected=simulation.algorithm == name)

    def draw_control_cards(self, screen, simulation, delay, benchmark,
                           grid_inputs, active_input, select_all,
                           grid_message, edit_mode):
        benchmark_y = CONTENT_TOP + 204
        self.draw_card(screen, (LEFT_X, benchmark_y, LEFT_WIDTH, 86), "Benchmark")
        self.draw_button(
            screen, "benchmark",
            "Chạy lại benchmark" if benchmark and benchmark.done
            else "Đang chạy..." if benchmark else "Chạy benchmark",
            style="primary", disabled=benchmark is not None and not benchmark.done,
        )

        edit_y = CONTENT_TOP + 304
        self.draw_card(screen, (LEFT_X, edit_y, LEFT_WIDTH, 242),
                       "Tạo và sửa bản đồ")
        self.draw_button(screen, "set_start", "Đặt Start",
                         selected=edit_mode == "start")
        self.draw_button(screen, "set_goal", "Đặt Goal",
                         selected=edit_mode == "goal")
        self.draw_button(screen, "random", "Tạo ngẫu nhiên")
        self.draw_button(screen, "weights", "Tạo trọng số")
        self.draw_button(screen, "clear", "Reset bản đồ", style="danger")

        speed_y = CONTENT_TOP + 560
        self.draw_card(
            screen,
            (LEFT_X, speed_y, LEFT_WIDTH, 108),
            "Tốc độ thuật toán",
        )
        self.draw_button(screen, "decrease", "−")
        self.draw_button(screen, "increase", "+")
        value_rect = pygame.Rect(LEFT_X + 69, CONTENT_TOP + 618, 72, 34)
        pygame.draw.rect(screen, INSET, value_rect, border_radius=6)
        value = self.button_bold.render(f"{delay} ms", True, TEXT)
        screen.blit(value, value.get_rect(center=value_rect.center))

    def draw_result_card(self, screen, simulation):
        rect = self.draw_card(
            screen, (RIGHT_X, CONTENT_TOP, RIGHT_WIDTH, 264),
            "Kết quả lần chạy",
        )
        show_result = simulation.result_visible
        path_length = (
            simulation.path_length
            if show_result and simulation.path_length is not None else "—"
        )
        cost = simulation.cost if show_result and simulation.cost is not None else "—"
        time = f"{simulation.time_ms:.3f} ms" if show_result else "—"
        values = (
            ("Thuật toán", simulation.algorithm or "—"),
            ("Thời gian", time),
            ("Node đã quét", simulation.scan_index),
            ("Độ dài đường đi", path_length),
            ("Tổng chi phí", cost),
        )
        for index, (label, value) in enumerate(values):
            self.draw_label_value(screen, label, value, rect.y + 51 + index * 27)

        metrics = simulation.metrics or {}
        self.draw_text(screen, f"Node đang xét: {metrics.get('position', '—')}",
                       (rect.x + 18, rect.y + 194), SECONDARY_TEXT, self.secondary)
        stat_y = rect.y + 222
        stat_width = (rect.width - 48) // 3
        for index, key in enumerate(("g", "h", "f")):
            box = pygame.Rect(rect.x + 16 + index * (stat_width + 8),
                              stat_y, stat_width, 29)
            pygame.draw.rect(screen, INSET, box, border_radius=6)
            value = metrics.get(key)
            rendered = self.stat.render(
                f"{key}: {value if value is not None else '—'}", True, BLUE_DARK
            )
            screen.blit(rendered, rendered.get_rect(center=box.center))

    def draw_benchmark_table(self, screen, benchmark, selected_algorithm):
        benchmark_y = CONTENT_TOP + 278
        legend_y = HEIGHT - MARGIN - 158
        rect = self.draw_card(
            screen,
            (RIGHT_X, benchmark_y, RIGHT_WIDTH,
             max(220, legend_y - GAP - benchmark_y)),
            "Benchmark",
        )
        if benchmark is None:
            # self.draw_text(screen, "Chưa có kết quả",
            #                (rect.x + 18, rect.y + 61), font=self.button_bold)
            # self.draw_text(
            #     screen, "Chạy benchmark để so sánh BFS, Dijkstra và A*.",
            #     (rect.x + 18, rect.y + 93), SECONDARY_TEXT, self.secondary,
            # )
            # flow = pygame.Rect(rect.x + 18, rect.y + 133,
            #                    rect.width - 36, 44)
            # pygame.draw.rect(screen, INSET, flow, border_radius=7)
            # rendered = self.button_bold.render(
            #     "BFS   →   Dijkstra   →   A*", True, TEXT
            # )
            # screen.blit(rendered, rendered.get_rect(center=flow.center))
            # self.draw_text(screen, "Quét → di chuyển → thuật toán kế tiếp",
            #                (rect.x + 18, rect.y + 204), MUTED, self.secondary)
            self.draw_text(screen, "Chưa có kết quả",
                           (rect.x + 18, rect.y + 61), font=self.button_bold)
            flow = pygame.Rect(rect.x + 18, rect.y + 133,
                               rect.width - 36, 44)
            pygame.draw.rect(screen, INSET, flow, border_radius=7)
            rendered = self.button_bold.render(
                "BFS   →   Dijkstra   →   A*", True, TEXT
            )
            screen.blit(rendered, rendered.get_rect(center=flow.center))
            return

        if not benchmark.done:
            completed, total = benchmark.progress
            names = ("BFS", "Dijkstra", "A*")
            name = names[min(completed, len(names) - 1)]
            self.draw_text(screen, f"Đang mô phỏng {name}",
                           (rect.x + 18, rect.y + 62), BLUE_DARK,
                           self.button_bold)
            self.draw_text(screen, f"Thuật toán {completed + 1}/{total}",
                           (rect.x + 18, rect.y + 94), MUTED, self.secondary)
            bar = pygame.Rect(rect.x + 18, rect.y + 132, rect.width - 36, 10)
            pygame.draw.rect(screen, SECONDARY_BUTTON, bar, border_radius=5)
            fill = bar.copy()
            fill.width = int(bar.width * completed / total)
            pygame.draw.rect(screen, PRIMARY, fill, border_radius=5)
            self.draw_text(screen, "Quét → di chuyển → thuật toán kế tiếp",
                           (rect.x + 18, rect.y + 170), SECONDARY_TEXT,
                           self.secondary)
            return

        table = pygame.Rect(rect.x + 12, rect.y + 50,
                            rect.width - 24, max(128, rect.height - 62))
        column_widths = (104, 68, 62, 58, 52)
        column_x = [table.x]
        for width in column_widths[:-1]:
            column_x.append(column_x[-1] + width)
        header_height = 30
        header = pygame.Rect(table.x, table.y, table.width, header_height)
        pygame.draw.rect(screen, SECONDARY_BUTTON, header, border_radius=6)
        headers = ("Thuật toán", "Time (ms)", "Nodes", "Path", "Cost")
        for index, title in enumerate(headers):
            align = "left" if index == 0 else "center"
            self._draw_table_cell(screen, title, column_x[index], table.y + 7,
                                  column_widths[index], align, MUTED)

        row_height = (table.height - header_height) // max(1, len(benchmark.results))
        for index, result in enumerate(benchmark.results):
            y = table.y + header_height + index * row_height
            row = pygame.Rect(table.x, y, table.width, row_height)
            if result["algorithm"] == selected_algorithm:
                pygame.draw.rect(screen, ROW_SELECTED, row, border_radius=5)
            pygame.draw.line(screen, CARD_BORDER,
                             (table.x, row.bottom), (table.right, row.bottom))
            values = (
                result["algorithm"], f'{result["time_ms"]:.3f}',
                result["nodes"],
                result["path_length"] if result["found"] else "—",
                result["cost"] if result["found"] else "—",
            )
            for cell_index, value in enumerate(values):
                align = "left" if cell_index == 0 else "center"
                self._draw_table_cell(
                    screen, value, column_x[cell_index], y + 14,
                    column_widths[cell_index], align, TEXT,
                )

    def _draw_table_cell(self, screen, value, x, y, width, align, color):
        rendered = self.secondary.render(str(value), True, color)
        if align == "left":
            screen.blit(rendered, (x + 8, y))
        else:
            screen.blit(rendered, rendered.get_rect(centerx=x + width // 2,
                                                    top=y))

    def draw_legend(self, screen):
        rect = self.draw_card(
            screen, (RIGHT_X, HEIGHT - MARGIN - 158, RIGHT_WIDTH, 158),
            "Chú thích",
        )
        entries = (
            (GREEN, "Điểm đầu"), (SCANNED_BLUE, "Ô đã quét"),
            ("flag", "Điểm đích"), (YELLOW, "Đường đã đi"),
            (BLACK, "Vật cản"), (None, "Xe"),
        )
        for index, (color, label) in enumerate(entries):
            x = rect.x + 18 + (index % 2) * ((rect.width - 36) // 2)
            y = rect.y + 49 + (index // 2) * 31
            if color == "flag":
                icon = pygame.transform.smoothscale(self.flag_source, (18, 18))
                screen.blit(icon, (x, y))
            elif color is None:
                icon = pygame.transform.smoothscale(self.car_icon, (9, 20))
                screen.blit(icon, (x + 4, y - 2))
            else:
                pygame.draw.rect(screen, color, (x, y, 18, 18))
                pygame.draw.rect(screen, CARD_BORDER, (x, y, 18, 18), 1)
            self.draw_text(screen, label, (x + 27, y), SECONDARY_TEXT,
                           self.secondary)

    def draw(self, screen, grid, simulation, delay, benchmark,
             grid_inputs=None, active_input=None, input_select_all=False,
             grid_message="", edit_mode="obstacle", mouse_position=None):
        configure_layout(grid)
        self.controls = create_controls()
        self.mouse_position = mouse_position or (-1, -1)
        grid_inputs = grid_inputs or {
            "rows": str(grid.rows), "columns": str(grid.columns),
        }
        screen.fill(BACKGROUND)
        self.draw_algorithm_card(screen, simulation)
        self.draw_control_cards(
            screen, simulation, delay, benchmark, grid_inputs,
            active_input, input_select_all, grid_message, edit_mode,
        )
        self.draw_map_card(screen, grid, simulation)
        self.draw_result_card(screen, simulation)
        self.draw_benchmark_table(screen, benchmark, simulation.algorithm)
        self.draw_legend(screen)


# FILE: src/simulation.py

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
        self._grid = grid
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
    def path_length(self):
        return len(self.path) - 1 if self.path else None

    @property
    def cost(self):
        if not self.path:
            return None
        return sum(self._grid.weight_at(position) for position in self.path[1:])


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


# FILE: tests/export.py

from pathlib import Path

repo = Path(".")
extensions = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}

with open("repo_context.md", "w", encoding="utf-8") as out:
    for path in sorted(repo.rglob("*")):
        if (
            path.is_file()
            and path.suffix.lower() in extensions
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and "venv" not in path.parts
            and ".venv" not in path.parts
            and "node_modules" not in path.parts
        ):
            out.write(f"\n\n# FILE: {path.as_posix()}\n\n")
            try:
                out.write(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                pass

# FILE: tests/test_algorithms.py

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


# FILE: tests/test_map_model.py

# Kiểm thử mô hình bản đồ.


# FILE: tests/test_simulation.py

# Kiểm thử mô phỏng xe.


# FILE: tests/test_ui.py

"""Kiểm tra sự kiện thật và các pha mô phỏng với Pygame headless."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import src.renderer as ui

from src.benchmark import BenchmarkRunner
from src.main import Application
from src.map_model import GridMap
from src.renderer import (
    BLACK, GRID_AREA, INSET, Renderer, grid_geometry,
    grid_panel_geometry, grid_position, window_viewport,
)
from src.simulation import Simulation


class SimulationTests(unittest.TestCase):
    def test_scan_finishes_before_car_moves_and_trail_is_kept(self):
        grid = GridMap(3, 3)
        grid.start, grid.goal = (0, 0), (2, 2)
        for algorithm in ("BFS", "Dijkstra", "A*"):
            with self.subTest(algorithm=algorithm):
                sim = Simulation(grid)
                sim.start(grid, algorithm, 0)
                now = 0
                while sim.phase == "scanning":
                    now += 15
                    sim.update(now, 10, scan_batch=1)
                    self.assertEqual(sim.car_position, grid.start)
                    self.assertFalse(sim.visible_path)
                self.assertEqual(sim.metrics["position"], grid.goal)
                for _ in range(len(sim.path)):
                    now += 10
                    sim.update(now, 10)
                self.assertEqual(sim.phase, "done")
                self.assertEqual(sim.car_position, grid.goal)
                self.assertEqual(sim.visible_path, set(sim.path))

    def test_no_path_and_start_equals_goal(self):
        grid = GridMap(2, 2)
        grid.start, grid.goal = (0, 0), (1, 1)
        grid.obstacles.update({(1, 0), (0, 1)})
        sim = Simulation(grid)
        sim.start(grid, "BFS", 0)
        sim.update(20, 10)
        self.assertEqual(sim.phase, "done")
        self.assertIsNone(sim.cost)
        self.assertFalse(sim.visible_path)
        grid.goal = grid.start
        sim.start(grid, "A*", 20)
        sim.update(40, 10)
        sim.update(60, 10)
        self.assertEqual(sim.phase, "done")
        self.assertEqual(sim.cost, 0)

    def test_benchmark_uses_snapshot_and_reports_failure(self):
        grid = GridMap(2, 2)
        grid.start, grid.goal = (0, 0), (1, 1)
        runner = BenchmarkRunner(grid, repetitions=2)
        grid.obstacles.update({(1, 0), (0, 1)})
        while not runner.done:
            runner.step()
        self.assertTrue(all(r["cost"] == 2 for r in runner.results))
        blocked = BenchmarkRunner(grid, repetitions=1)
        while not blocked.done:
            blocked.step()
        self.assertTrue(all(not r["found"] and r["cost"] is None
                            and r["path_length"] is None for r in blocked.results))


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        cls.renderer = Renderer()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.app = Application()
        self.app.grid.start = (0, 7)
        self.app.grid.goal = (20, 29)
        self.app.simulation.reset(self.app.grid)
        self.canvas = pygame.Surface(ui.layout_size())
        self.viewport = window_viewport((1200, 760), ui.layout_size())

    def click(self, position, button=1, now=0):
        logical_width, logical_height = ui.layout_size()
        self.viewport = window_viewport((1200, 760), ui.layout_size())
        x = self.viewport.x + round(
            position[0] * self.viewport.width / logical_width
        )
        y = self.viewport.y + round(
            position[1] * self.viewport.height / logical_height
        )
        self.app.handle_event(
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y), button=button),
            self.viewport, now,
        )

    def test_benchmark_button_runs_three_and_edit_invalidates(self):
        self.click(self.app.controls["benchmark"].center)
        self.assertIsNotNone(self.app.benchmark)
        self.assertEqual(self.app.simulation.phase, "idle")
        phases = {name: [] for name in ("BFS", "Dijkstra", "A*")}
        for frame in range(5000):
            self.app.update(frame * 50)
            sim = self.app.simulation
            if sim.algorithm and (not phases[sim.algorithm]
                                  or phases[sim.algorithm][-1] != sim.phase):
                phases[sim.algorithm].append(sim.phase)
            if self.app.benchmark.done:
                break
            self.assertEqual(self.app.benchmark.results, [])
        self.assertTrue(self.app.benchmark.done)
        for sequence in phases.values():
            self.assertEqual(sequence, ["scanning", "moving", "done"])
        results = self.app.benchmark.results
        self.assertEqual([r["algorithm"] for r in results], ["BFS", "Dijkstra", "A*"])
        self.assertTrue(all(r["cost"] == 42 and r["nodes"] > 0 for r in results))
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, self.app.benchmark)
        cell_width, cell_height, grid_rect = grid_geometry(self.app.grid)
        self.click((grid_rect.x + cell_width / 2,
                    grid_rect.y + cell_height / 2))
        self.assertIn((0, 0), self.app.grid.obstacles)
        self.assertIsNone(self.app.benchmark)

    def test_benchmark_can_be_cancelled_by_edit_or_algorithm(self):
        for action in ("clear", "random", "BFS"):
            self.click(self.app.controls["benchmark"].center)
            self.app.update(20)
            self.click(self.app.controls[action].center, now=30)
            self.assertIsNone(self.app.benchmark)

    def test_benchmark_finishes_when_no_route_exists(self):
        self.app.grid.obstacles.update({(0, 6), (0, 8), (1, 7)})
        self.click(self.app.controls["benchmark"].center)
        for frame in range(5000):
            self.app.update(frame * 50)
            if self.app.benchmark.done:
                break
        self.assertTrue(self.app.benchmark.done)
        self.assertTrue(all(not result["found"] for result in self.app.benchmark.results))
        self.assertFalse(self.app.simulation.visible_path)

    def test_resized_clicks_controls_and_restart(self):
        self.click(self.app.controls["increase"].center)
        self.assertEqual(self.app.path_step_delay, 60)
        self.click(self.app.controls["decrease"].center)
        self.assertEqual(self.app.path_step_delay, 50)
        for name in ("BFS", "Dijkstra", "A*"):
            self.click(self.app.controls[name].center)
            self.assertEqual(self.app.simulation.algorithm, name)
            self.assertEqual(self.app.simulation.phase, "scanning")
            self.app.update(20)
            self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                               self.app.path_step_delay, self.app.benchmark)
        self.click(self.app.controls["clear"].center)
        self.assertEqual(self.app.simulation.phase, "idle")
        self.assertFalse(self.app.grid.obstacles)
        self.assertFalse(self.app.simulation.scanned_cells)
        self.click(self.app.controls["random"].center)
        self.assertTrue(self.app.grid.obstacles)
        _, _, grid_rect = grid_geometry(self.app.grid)
        self.assertIsNone(grid_position((grid_rect.x - 1, grid_rect.y), self.app.grid))
        self.assertIsNone(grid_position((grid_rect.x, grid_rect.y - 1), self.app.grid))

    def test_custom_grid_inputs_validation_and_creation(self):
        self.click(self.app.controls["rows_input"].center)
        self.assertTrue(self.app.input_select_all)
        for digit in "12":
            self.app.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=ord(digit), unicode=digit),
                self.viewport, 0,
            )
        self.click(self.app.controls["columns_input"].center)
        self.assertTrue(self.app.input_select_all)
        for digit in "18":
            self.app.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=ord(digit), unicode=digit),
                self.viewport, 0,
            )
        self.click(self.app.controls["apply_grid"].center)
        self.assertEqual((self.app.grid.rows, self.app.grid.columns), (12, 18))
        self.assertEqual(self.app.grid.start, (0, 0))
        self.assertEqual(self.app.grid.goal, (11, 17))
        self.assertEqual(self.app.simulation.car_position, (0, 0))
        self.app.grid_inputs["rows"] = "4"
        self.app.create_custom_grid()
        self.assertTrue(self.app.grid_message.startswith("Lỗi"))
        self.assertEqual((self.app.grid.rows, self.app.grid.columns), (12, 18))

        self.app.grid_inputs = {"rows": "50", "columns": "50"}
        self.app.create_custom_grid()
        cell_width, cell_height, rect = grid_geometry(self.app.grid)
        self.assertGreater(cell_width, 0)
        self.assertGreater(cell_height, 0)
        self.assertLessEqual(rect.width, GRID_AREA.width)
        self.assertLessEqual(rect.height, GRID_AREA.height)

    def test_grid_cells_stay_square_for_different_dimensions(self):
        for rows, columns in ((5, 80), (50, 5), (25, 50), (50, 50)):
            self.app.grid_inputs = {
                "rows": str(rows), "columns": str(columns),
            }
            self.app.create_custom_grid()
            cell_width, cell_height, rect = grid_geometry(self.app.grid)
            self.assertGreater(cell_width, 0)
            self.assertGreater(cell_height, 0)
            self.assertLessEqual(rect.width, GRID_AREA.width)
            self.assertLessEqual(rect.height, GRID_AREA.height)
            panel = grid_panel_geometry(self.app.grid)
            self.assertGreaterEqual(panel.width, rect.width + 28)
            self.assertEqual(panel.top, ui.CONTENT_TOP)
            self.assertEqual(panel.bottom, ui.HEIGHT - ui.MARGIN)
            self.assertEqual(panel.centerx, rect.centerx)
            self.assertGreaterEqual(rect.top - panel.top, 14)

    def test_reset_preserves_start_and_goal(self):
        self.app.grid.start = (3, 4)
        self.app.grid.goal = (20, 40)
        self.app.grid.obstacles.update({(5, 5), (6, 6)})
        self.app.grid.set_weight((7, 7), 4)
        self.click(self.app.controls["clear"].center)
        self.assertEqual(self.app.grid.start, (3, 4))
        self.assertEqual(self.app.grid.goal, (20, 40))
        self.assertFalse(self.app.grid.obstacles)
        self.assertFalse(self.app.grid.weights)

    def test_user_can_place_start_and_goal(self):
        cell_width, cell_height, rect = grid_geometry(self.app.grid)

        def center(row, column):
            return (rect.x + (column + 0.5) * cell_width,
                    rect.y + (row + 0.5) * cell_height)

        self.app.grid.obstacles.update({(3, 4), (20, 40)})
        self.click(self.app.controls["set_start"].center)
        self.assertEqual(self.app.edit_mode, "start")
        self.click(center(3, 4))
        self.assertEqual(self.app.grid.start, (3, 4))
        self.assertNotIn((3, 4), self.app.grid.obstacles)
        self.assertEqual(self.app.edit_mode, "obstacle")

        self.click(self.app.controls["set_goal"].center)
        self.click(center(20, 40))
        self.assertEqual(self.app.grid.goal, (20, 40))
        self.assertNotIn((20, 40), self.app.grid.obstacles)
        self.assertEqual(self.app.simulation.car_position, (3, 4))

        self.click(self.app.controls["set_start"].center)
        self.click(center(20, 40))
        self.assertTrue(self.app.grid_message.startswith("Lỗi"))
        self.assertEqual(self.app.grid.start, (3, 4))

    def test_render_preserves_obstacle_seam_and_loads_car(self):
        self.app.grid.obstacles.update({(0, 0), (0, 1)})
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, None)
        cell_width, cell_height, grid_rect = grid_geometry(self.app.grid)
        boundary = grid_rect.x + round(cell_width)
        for x in (boundary - 1, boundary):
            self.assertEqual(self.canvas.get_at((x, grid_rect.y + 5))[:3], BLACK)
        car_size = round(min(cell_width, cell_height))
        car_images = self.renderer.car_images(car_size)
        self.assertEqual(len(car_images), 4)
        for sprite in car_images.values():
            self.assertLessEqual(max(sprite.get_size()), car_size)
            self.assertTrue(sprite.get_flags() & pygame.SRCALPHA)

    def test_empty_benchmark_card_keeps_its_content_area(self):
        self.renderer.draw(self.canvas, self.app.grid, self.app.simulation,
                           self.app.path_step_delay, None)
        self.assertEqual(
            self.canvas.get_at((ui.RIGHT_X + 30, 450))[:3],
            INSET,
        )
