import random

import pygame

from algorithms import a_star, bfs, dijkstra
from map_model import GridMap
from renderer import (
    CELL_SIZE,
    PANEL_HEIGHT,
    WHITE,
    create_buttons,
    create_clear_button,
    create_random_button,
    create_speed_buttons,
    draw_grid,
    draw_panel,
    set_font,
)


ROWS = 25
COLUMNS = 50
GRID_WIDTH = COLUMNS * CELL_SIZE
WIDTH = GRID_WIDTH
HEIGHT = ROWS * CELL_SIZE + PANEL_HEIGHT

PATH_STEP_DELAY = 50


def create_demo_map():
    grid = GridMap(ROWS, COLUMNS)
    grid.start = (0, 7)
    grid.goal = (20, 29)

    grid.obstacles.update({
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 7),
        (6, 8),
        (6, 9),
    })

    return grid


def generate_random_street_map(grid):
    grid.obstacles.clear()

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

def get_path(grid, selected_algorithm):
    algorithms = {
        "BFS": bfs,
        "Dijkstra": dijkstra,
        "A*": a_star,
    }

    algorithm = algorithms[selected_algorithm]
    try:
        path = algorithm(grid)
    except NotImplementedError:
        return [], f"{selected_algorithm} chưa được cài đặt"

    if path is None:
        return [], "Không tìm thấy đường"

    return path, f"Đang chạy {selected_algorithm}..."


def get_grid_position(mouse_position, grid):
    mouse_x, mouse_y = mouse_position

    if mouse_x >= GRID_WIDTH:
        return None

    if mouse_y < PANEL_HEIGHT:
        return None

    row = (mouse_y - PANEL_HEIGHT) // CELL_SIZE
    column = mouse_x // CELL_SIZE
    position = (row, column)

    if grid.is_inside(position):
        return position

    return None


def edit_obstacle(grid, mouse_position, add_obstacle):
    position = get_grid_position(mouse_position, grid)

    if position is None or position in (grid.start, grid.goal):
        return False

    was_obstacle = grid.is_obstacle(position)

    if add_obstacle:
        grid.obstacles.add(position)
    else:
        grid.obstacles.discard(position)

    return was_obstacle != add_obstacle


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mô phỏng xe tìm đường tự động")

    font = set_font(24, bold=True)
    small_font = set_font(18)

    grid = create_demo_map()
    buttons = create_buttons(GRID_WIDTH)
    random_button = create_random_button(GRID_WIDTH, HEIGHT)
    clear_button = create_clear_button(GRID_WIDTH, HEIGHT)
    speed_buttons = create_speed_buttons(GRID_WIDTH)

    selected_algorithm = None
    status = "Chọn thuật toán"

    path_step_delay = PATH_STEP_DELAY
    full_path = []
    visible_path = set()
    car_position = grid.start
    path_index = 0
    last_path_step = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                map_changed = False

                if event.button == 1:
                    if speed_buttons["decrease"].collidepoint(event.pos):
                        path_step_delay = max(10, path_step_delay - 10)
                    elif speed_buttons["increase"].collidepoint(event.pos):
                        path_step_delay = min(500, path_step_delay + 10)
                    elif random_button.collidepoint(event.pos):
                        generate_random_street_map(grid)
                        selected_algorithm = None
                        full_path = []
                        visible_path.clear()
                        car_position = grid.start
                        path_index = 0
                        status = "Đã tạo bản đồ đường phố ngẫu nhiên"

                    elif clear_button.collidepoint(event.pos):
                        grid.obstacles.clear()
                        selected_algorithm = None
                        full_path = []
                        visible_path.clear()
                        car_position = grid.start
                        path_index = 0
                        status = "Đã xóa toàn bộ bản đồ"
                    else:
                        for algorithm_name, button_rect in buttons.items():
                            if button_rect.collidepoint(event.pos):
                                selected_algorithm = algorithm_name
                                full_path, status = get_path(
                                    grid,
                                    selected_algorithm
                                )
                                visible_path.clear()
                                car_position = grid.start
                                path_index = 0
                                last_path_step = pygame.time.get_ticks()
                                break

                        map_changed = edit_obstacle(grid, event.pos, True)

                elif event.button == 3:
                    map_changed = edit_obstacle(grid, event.pos, False)

                if map_changed:
                    selected_algorithm = None
                    full_path = []
                    visible_path.clear()
                    car_position = grid.start
                    path_index = 0
                    status = "Bản đồ đã thay đổi"

            elif event.type == pygame.MOUSEMOTION:
                left_pressed, _, right_pressed = event.buttons
                map_changed = False

                if left_pressed:
                    map_changed = edit_obstacle(grid, event.pos, True)
                elif right_pressed:
                    map_changed = edit_obstacle(grid, event.pos, False)

                if map_changed:
                    selected_algorithm = None
                    full_path = []
                    visible_path.clear()
                    car_position = grid.start
                    path_index = 0
                    status = "Bản đồ đã thay đổi"

        current_time = pygame.time.get_ticks()

        if (path_index < len(full_path)
                and current_time - last_path_step >= path_step_delay):
            visible_path.add(full_path[path_index])
            car_position = full_path[path_index]
            path_index += 1
            last_path_step = current_time
            if path_index == len(full_path):
                number_of_steps = max(0, len(full_path) - 1)
                status = f"{selected_algorithm}: {number_of_steps} bước"

        screen.fill(WHITE)
        draw_grid(screen, grid, visible_path, car_position, PANEL_HEIGHT)
        draw_panel(
            screen,
            GRID_WIDTH,
            PANEL_HEIGHT,
            buttons,
            random_button,
            clear_button,
            selected_algorithm,
            font,
            small_font,
            status,
            speed_buttons,
            path_step_delay
        )

        pygame.display.flip()
        clock.tick(144)

    pygame.quit()


if __name__ == "__main__":
    main()
