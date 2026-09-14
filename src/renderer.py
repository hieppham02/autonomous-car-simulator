import pygame


CELL_SIZE = 50
PANEL_WIDTH = 220

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
BLACK = (50, 50, 50)
YELLOW = (255, 220, 0)
BLUE = (50, 120, 220)
DARK_BLUE = (30, 80, 160)
DARK_GRAY = (45, 55, 72)


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
        "BFS": pygame.Rect(grid_width + 30, 90, 160, 50),
        "Dijkstra": pygame.Rect(grid_width + 30, 160, 160, 50),
        "A*": pygame.Rect(grid_width + 30, 230, 160, 50),
    }


def draw_grid(screen, grid, visible_path):
    for row in range(grid.rows):
        for column in range(grid.columns):
            position = (row, column)
            x = column * CELL_SIZE
            y = row * CELL_SIZE
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


def draw_button(screen, rect, text, font, is_selected):
    color = DARK_BLUE if is_selected else BLUE

    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_panel(
    screen,
    grid_width,
    panel_height,
    buttons,
    selected_algorithm,
    font,
    small_font,
    status
):
    panel_rect = pygame.Rect(grid_width, 0, PANEL_WIDTH, panel_height)
    pygame.draw.rect(screen, DARK_GRAY, panel_rect)

    title = font.render("THUẬT TOÁN", True, WHITE)
    title_position = (grid_width + PANEL_WIDTH // 2, 45)
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
    screen.blit(status_surface, (grid_width + 18, 330))
