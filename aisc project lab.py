import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game with AI Pathfinding & Score Display')
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.SysFont(None, 30)

# Snake direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False
        self.score = 0

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Add new head to the snake's body
        self.body.insert(0, new_head)

        # If not growing, remove the tail
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True
        self.score += 1  # Increase score when the snake eats the food

    def check_collision(self):
        head_x, head_y = self.body[0]
        if not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT):
            return True
        if len(self.body) != len(set(self.body)):
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# BFS for AI pathfinding
def bfs(snake, food_pos):
    start = snake.body[0]
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (current, path) = queue.popleft()

        # If we reached the food, return the path
        if current == food_pos:
            return path

        # Explore neighbors
        for direction in [UP, DOWN, LEFT, RIGHT]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT and
                    neighbor not in snake.body and neighbor not in visited):
                queue.append((neighbor, path + [direction]))
                visited.add(neighbor)

    # No path found
    return None

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

# Function to draw the snake, food, and score
def draw_objects(snake, food):
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw score
    score_text = font.render(f"Score: {snake.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
def main():
    snake = Snake()
    food = Food()
    ai_enabled = True  # Toggle AI control
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                    ai_enabled = False
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                    ai_enabled = False
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                    ai_enabled = False
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                    ai_enabled = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    food.position = (x // CELL_SIZE, y // CELL_SIZE)

        if not game_over:
            if ai_enabled:
                # Get AI's path to food
                path = bfs(snake, food.position)
                if path:
                    snake.change_direction(path[0])

            # Move the snake
            snake.move()

            # Check for collisions
            if snake.check_collision():
                game_over = True

            # Check if snake eats the food
            if snake.body[0] == food.position:
                snake.grow_snake()
                food.randomize_position()

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_objects(snake, food)

        # Show "Game Over" message if game is over
        if game_over:
            game_over_text = font.render("Game Over! Press ESC to exit", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()

        pygame.display.flip()

        # Handle exiting the game after "Game Over"
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Control the game's speed
        clock.tick(10)

if __name__ == "__main__":
    main()