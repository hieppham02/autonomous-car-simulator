"""Hiển thị grid map, đường đi và bảng điều khiển bằng Pygame."""

import pygame


CELL_SIZE = 20
PANEL_HEIGHT = 125

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
BLACK = (50, 50, 50)
YELLOW = (255, 220, 0)
BLUE = (50, 120, 220)
CAR_BLUE = (20, 85, 200)
DARK_BLUE = (30, 80, 160)
DARK_GRAY = (45, 55, 72)
CLEAR_RED = (185, 55, 55)


def set_font(size, bold=False):
    font_path = pygame.font.match_font([
        "segoeui",
        "arial",
        "dejavusans"
    ])

    if font_path is None:
        font = pygame.font.Font(None, size)
    else:
        font = pygame.font.Font(font_path, size)

    font.set_bold(bold)
    return font


def create_buttons(grid_width):
    return {
        "BFS": pygame.Rect(160, 14, 115, 38),
        "Dijkstra": pygame.Rect(285, 14, 125, 38),
        "A*": pygame.Rect(420, 14, 100, 38),
    }


def create_clear_button(grid_width, panel_height):
    return pygame.Rect(
        grid_width - 170,
        14,
        150,
        38
    )


def create_random_button(grid_width, panel_height):
    return pygame.Rect(
        grid_width - 350,
        14,
        170,
        38
    )


def create_speed_buttons(grid_width):
    return {
        "decrease": pygame.Rect(grid_width - 290, 76, 36, 32),
        "increase": pygame.Rect(grid_width - 126, 76, 36, 32),
    }


def draw_grid(screen, grid, visible_path, car_position=None, offset_y=0):
    for row in range(grid.rows):
        for column in range(grid.columns):
            position = (row, column)
            x = column * CELL_SIZE
            y = offset_y + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            color = WHITE

            if position == grid.start:
                color = GREEN
            elif position == grid.goal:
                color = RED
            elif grid.is_obstacle(position):
                color = BLACK
            elif position in visible_path:
                color = YELLOW

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    if car_position is not None:
        row, column = car_position
        center = (
            column * CELL_SIZE + CELL_SIZE // 2,
            offset_y + row * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(screen, CAR_BLUE, center, CELL_SIZE // 2 - 2)
        pygame.draw.circle(screen, WHITE, center, 3)



def draw_button(screen, rect, text, font, is_selected=False, color=BLUE):
    button_color = DARK_BLUE if is_selected else color

    pygame.draw.rect(screen, button_color, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_panel(
    screen,
    grid_width,
    panel_height,
    buttons,
    random_button,
    clear_button,
    selected_algorithm,
    font,
    small_font,
    status,
    speed_buttons=None,
    path_step_delay=50
):
    panel_rect = pygame.Rect(0, 0, grid_width, panel_height)
    pygame.draw.rect(screen, DARK_GRAY, panel_rect)

    title = font.render("THUẬT TOÁN", True, WHITE)
    title_position = (75, 33)
    screen.blit(title, title.get_rect(center=title_position))

    for algorithm_name, button_rect in buttons.items():
        draw_button(
            screen,
            button_rect,
            algorithm_name,
            font,
            algorithm_name == selected_algorithm
        )

    status_surface = small_font.render(status, True, WHITE)
    screen.blit(status_surface, (20, 82))

    if speed_buttons:
        speed_label = small_font.render("Tốc độ:", True, WHITE)
        screen.blit(speed_label, (grid_width - 390, 82))
        draw_button(screen, speed_buttons["decrease"], "-", small_font)
        draw_button(screen, speed_buttons["increase"], "+", small_font)

        value_rect = pygame.Rect(grid_width - 246, 76, 112, 32)
        pygame.draw.rect(screen, WHITE, value_rect, border_radius=4)
        pygame.draw.rect(screen, BLACK, value_rect, 2, border_radius=4)
        value_text = small_font.render(f"{path_step_delay} ms", True, BLACK)
        screen.blit(value_text, value_text.get_rect(center=value_rect.center))

    draw_button(
        screen,
        random_button,
        "TẠO NGẪU NHIÊN",
        small_font
    )

    draw_button(
        screen,
        clear_button,
        "XÓA TẤT CẢ",
        small_font,
        color=CLEAR_RED
    )
