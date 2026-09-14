import pygame

from map_model import GridMap

ROWS = 10
COLUMNS = 16
CELL_SIZE = 50
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)


def draw_grid(screen, grid):
    for row in range(grid.rows):
        for column in range(grid.columns):
            x = column * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, WHITE, rect, 3)
            pygame.draw.rect(screen, GRAY, rect, 1)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid Map")

    grid = GridMap(ROWS, COLUMNS)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_grid(screen, grid)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()