import sys
import pygame
from pygame.locals import *
import random
pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('3D Snake Game')

# Define grid properties
tile_width = 64
tile_height = 32
grid_rows = 10
grid_columns = 10

# Initialize snake properties
snake = [(4, 4), (4, 5), (4, 6)]
snake_color = (0, 255, 0)

# Initialize food properties
food_position = (random.randint(0, grid_rows - 1), random.randint(0, grid_columns - 1))
food_color = (255, 0, 0)

def draw_isometric_grid(screen, tile_width, tile_height, grid_rows, grid_columns, snake, food_position):
    # Calculate the grid offset to center it
    grid_width = (grid_columns - grid_rows) * (tile_width // 2)
    grid_height = (grid_columns + grid_rows) * (tile_height // 2)
    offset_x = (WINDOW_SIZE[0] - grid_width) // 2
    offset_y = (WINDOW_SIZE[1] - grid_height) // 2

    for row in range(grid_rows):
        for column in range(grid_columns):
            x = (column - row) * (tile_width // 2) + offset_x
            y = (column + row) * (tile_height // 2) + offset_y
            pygame.draw.polygon(screen, (0, 0, 255), [
                (x, y),
                (x + tile_width // 2, y + tile_height // 2),
                (x, y + tile_height),
                (x - tile_width // 2, y + tile_height // 2)
            ], 1)

            # Draw the snake
            if (row, column) in snake:
                pygame.draw.circle(screen, snake_color, (x, y), tile_width // 4)

            # Draw the food
            if (row, column) == food_position:
                pygame.draw.circle(screen, food_color, (x, y), tile_width // 4)

    return offset_x, offset_y

def move_snake(snake, direction):
    head = snake[0]
    if direction == "up":
        new_head = (head[0] - 1, head[1])
    elif direction == "down":
        new_head = (head[0] + 1, head[1])
    elif direction == "left":
        new_head = (head[0], head[1] - 1)
    elif direction == "right":
        new_head = (head[0], head[1] + 1)

    return [new_head] + snake[:-1]

def spawn_food(snake, grid_rows, grid_columns):
    food_position = (random.randint(0, grid_rows - 1), random.randint(0, grid_columns - 1))
    while food_position in snake:
        food_position = (random.randint(0, grid_rows - 1), random.randint(0, grid_columns - 1))

    return food_position

def main():
    global snake, food_position
    direction = "up"
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 255,255))

        # Draw the isometric grid, snake, and food
        offset_x, offset_y = draw_isometric_grid(screen, tile_width, tile_height, grid_rows, grid_columns, snake, food_position)

        # Update the display
        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:  # Move up
                    direction = "up"
                elif event.key == K_a:  # Move left
                    direction = "left"
                elif event.key == K_s:  # Move down
                    direction = "down"
                elif event.key == K_d:  # Move right
                    direction = "right"

        # Move the snake
        new_snake = move_snake(snake, direction)

        # Check for collisions with food
        if new_snake[0] == food_position:
            food_position = spawn_food(new_snake, grid_rows, grid_columns)
            snake = [new_snake[0]] + snake  # Grow the snake
        else:
            snake = new_snake

        # Check for collisions with self or walls
        head = snake[0]
        if head in snake[1:] or head[0] < 0 or head[0] >= grid_rows or head[1] < 0 or head[1] >= grid_columns:
            print("Game Over!")
            pygame.quit()
            sys.exit()

        clock.tick(5)  # Control the game speed
            
if __name__ == "__main__":
    main()