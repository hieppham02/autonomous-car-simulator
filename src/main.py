import pygame

from algorithms import bfs
from map_model import GridMap
from renderer import (
    CELL_SIZE,
    PANEL_WIDTH,
    WHITE,
    create_buttons,
    draw_grid,
    draw_panel,
    set_font,
)


ROWS = 10
COLUMNS = 16
GRID_WIDTH = COLUMNS * CELL_SIZE
WIDTH = GRID_WIDTH + PANEL_WIDTH
HEIGHT = ROWS * CELL_SIZE

PATH_STEP_DELAY = 120


def create_demo_map():
    grid = GridMap(ROWS, COLUMNS)
    grid.start = (0, 7)
    grid.goal = (8, 9)

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


def get_path(grid, selected_algorithm):
    if selected_algorithm == "BFS":
        path = bfs(grid)

        if path is None:
            return [], "Không tìm thấy đường"

        return path, "Đang chạy thuật toán BFS"

    return [], f"{selected_algorithm} chưa được cài đặt"


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mô phỏng xe tìm đường tự động")

    font = set_font(24, bold=True)
    small_font = set_font(18)

    grid = create_demo_map()
    buttons = create_buttons(GRID_WIDTH)

    selected_algorithm = None
    status = "Chọn thuật toán"

    full_path = []
    visible_path = set()
    path_index = 0
    last_path_step = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for algorithm_name, button_rect in buttons.items():
                    if button_rect.collidepoint(event.pos):
                        selected_algorithm = algorithm_name
                        full_path, status = get_path(grid, selected_algorithm)

                        visible_path.clear()
                        path_index = 0
                        last_path_step = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()

        if (
            path_index < len(full_path)
            and current_time - last_path_step >= PATH_STEP_DELAY
        ):
            visible_path.add(full_path[path_index])
            path_index += 1
            last_path_step = current_time

            if path_index == len(full_path):
                number_of_steps = max(0, len(full_path) - 1)
                status = f"Tìm thấy đích sau {number_of_steps} bước"

        screen.fill(WHITE)
        draw_grid(screen, grid, visible_path)
        draw_panel(
            screen,
            GRID_WIDTH,
            HEIGHT,
            buttons,
            selected_algorithm,
            font,
            small_font,
            status
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
