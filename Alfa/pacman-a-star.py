import pygame
import math
import time
from board import boards
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Define the preset map (0 for path, 1 for barrier)
# Creating a 31x31 maze-like pattern
PRESET_MAP = [[0 for _ in range(31)] for _ in range(31)]

# Add some example walls to create a maze pattern
# Vertical walls
for i in range(5, 25, 5):
    for j in range(31):
        if j % 3 != 0:  # Leave gaps for paths
            PRESET_MAP[j][i] = 1

# Horizontal walls
for i in range(5, 25, 5):
    for j in range(31):
        if j % 4 != 0:  # Leave gaps for paths
            PRESET_MAP[i][j] = 1

# Add some random obstacles
import random
random.seed(42)  # Use a fixed seed for reproducibility
for _ in range(100):
    x = random.randint(0, 30)
    y = random.randint(0, 30)
    if x % 3 != 0 and y % 3 != 0:  # Ensure we don't block all paths
        PRESET_MAP[y][x] = 1

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [
            (0, 1),  # Down
            (0, -1),  # Up
            (1, 0),  # Right
            (-1, 0)  # Left
        ]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < self.total_rows and 0 <= c < self.total_rows and not grid[r][c].is_barrier():
                self.neighbors.append(grid[r][c])

    def __lt__(self, other):
        return False

def move_start(grid, start, direction):
    if not start:
        return start
    
    row, col = start.get_pos()
    new_row, new_col = row, col
    
    if direction == "UP" and col > 0:
        new_col = col - 1
    elif direction == "DOWN" and col < start.total_rows - 1:
        new_col = col + 1
    elif direction == "LEFT" and row > 0:
        new_row = row - 1
    elif direction == "RIGHT" and row < start.total_rows - 1:
        new_row = row + 1
    
    # Check if the new position is valid (not a barrier or end point)
    if not grid[new_row][new_col].is_barrier() and not grid[new_row][new_col].is_end():
        start.reset()  # Reset the old position
        start = grid[new_row][new_col]
        start.make_start()
    
    return start

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current is not None:
            current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        _, current = frontier.get()

        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + h(neighbor.get_pos(), end.get_pos())
                frontier.put((priority, neighbor))
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows  # Ukuran cell grid
    for i in range(rows):
        grid.append([])
        for j in range(len(boards[i])):  # Iterasi berdasarkan board preset
            spot = Spot(i, j, gap, rows)
            if boards[i][j] == 0:  # Empty rectangle
                pass  # Biarkan cell kosong
            elif boards[i][j] == 1:  # Dot
                pass  # Anda bisa menambahkan dekorasi untuk dot jika perlu
            elif boards[i][j] == 2:  # Big dot
                pass  # Sama seperti di atas
            else:
                spot.make_barrier()  # Buat penghalang untuk jenis lain
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    return y // gap, x // gap


def make_grid_from_board(board, rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            # Set the color or type of the spot based on the board definition
            if i < len(board) and j < len(board[0]):
                board_value = board[i][j]
                if board_value == 0:  # Empty space
                    pass  # Leave as default (WHITE)
                elif board_value == 1:  # Dot (treat as a walkable path)
                    pass  # Can be customized to a specific color if needed
                elif board_value == 2:  # Big dot (also a walkable path)
                    pass  # Can use a special color or marker if desired
                elif board_value in {3, 4, 5, 6, 7, 8, 9}:  # Obstacles (walls or gates)
                    spot.make_barrier()
            grid[i].append(spot)
    return grid


def main(win, width):
    ROWS = len(boards)  # Use the number of rows in the board
    grid = make_grid_from_board(boards, ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end and not spot.is_barrier():
                    start = spot
                    start.make_start()
                elif not end and spot != start and not spot.is_barrier():
                    end = spot
                    end.make_end()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if spot != start and spot != end and not spot.is_barrier():
                    spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # Start stopwatch here
                    start_time = time.time()

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    # Stop stopwatch after algorithm finishes
                    elapsed_time = time.time() - start_time
                    print(f"Grid update took {elapsed_time:.2f} seconds.")

                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid_from_board(boards, ROWS, width)

                # Handle arrow key movements
                if start:
                    if event.key == pygame.K_UP:
                        start = move_start(grid, start, "UP")
                    elif event.key == pygame.K_DOWN:
                        start = move_start(grid, start, "DOWN")
                    elif event.key == pygame.K_LEFT:
                        start = move_start(grid, start, "LEFT")
                    elif event.key == pygame.K_RIGHT:
                        start = move_start(grid, start, "RIGHT")

                    # Update neighbors and redraw after movement
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    draw(win, grid, ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Pathfinding Algorithm")
    main(WIN, WIDTH)
