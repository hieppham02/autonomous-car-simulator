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
