import pygame as pg 
import random
from time import sleep

SCR_WIDTH = 500
SCR_HEIGHT = 500
FPS = 30
GRID_WIDTH = 400
GRID_CELL_WIDTH = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIME = (191, 255, 0)
BLUE = (0, 0, 255)
SCARLET = (255, 36, 0)

pg.init()
screen = pg.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pg.display.set_caption("Maze Generator")

def init_grid():                                                   
    grid = []
    for i in range(GRID_WIDTH // GRID_CELL_WIDTH + 1):
        x = SCR_WIDTH // 2 - GRID_WIDTH // 2 - GRID_CELL_WIDTH // 2 
        if i:
            y += GRID_CELL_WIDTH
        else:
            y = SCR_HEIGHT // 2 - GRID_WIDTH // 2 - GRID_CELL_WIDTH // 2

        for j in range(GRID_WIDTH // GRID_CELL_WIDTH + 1):                
            pg.draw.line(screen, WHITE, (x, y), (x + GRID_CELL_WIDTH, y))
            pg.draw.line(screen, WHITE, (x + GRID_CELL_WIDTH, y), (x + GRID_CELL_WIDTH, y + GRID_CELL_WIDTH))    
            pg.draw.line(screen, WHITE, (x + GRID_CELL_WIDTH, y + GRID_CELL_WIDTH), (x, y + GRID_CELL_WIDTH))   
            pg.draw.line(screen, WHITE, (x, y + GRID_CELL_WIDTH), (x, y)) 
            grid.append((x, y))                                            
            x += GRID_CELL_WIDTH

    return grid

def get_neighbors(x, y, visited, grid):
    neighbors = []

    if (x + GRID_CELL_WIDTH, y) not in visited and (x + GRID_CELL_WIDTH, y) in grid:
        neighbors.append("right")
    if (x - GRID_CELL_WIDTH, y) not in visited and (x - GRID_CELL_WIDTH, y) in grid:
        neighbors.append("left")
    if (x, y + GRID_CELL_WIDTH) not in visited and (x, y + GRID_CELL_WIDTH) in grid:
        neighbors.append("down")
    if (x, y - GRID_CELL_WIDTH) not in visited and (x, y - GRID_CELL_WIDTH) in grid:
        neighbors.append("up")

    return neighbors

def push_right(x, y):
    pg.draw.rect(screen, BLUE, (x + 1, y + 1, 2 * GRID_CELL_WIDTH - 1, GRID_CELL_WIDTH - 1))
    pg.display.update()

def push_left(x, y):
    pg.draw.rect(screen, BLUE, (x - GRID_CELL_WIDTH + 1, y + 1, 2 * GRID_CELL_WIDTH - 1, GRID_CELL_WIDTH - 1))
    pg.display.update()

def push_up(x, y):
    pg.draw.rect(screen, BLUE, (x + 1, y - GRID_CELL_WIDTH + 1, GRID_CELL_WIDTH - 1, 2 * GRID_CELL_WIDTH - 1))
    pg.display.update()

def push_down(x, y):
    pg.draw.rect(screen, BLUE, (x + 1, y + 1, GRID_CELL_WIDTH - 1, 2 * GRID_CELL_WIDTH - 1))
    pg.display.update()

def single_cell(x, y):
    pg.draw.rect(screen, LIME, (x + 1, y + 1, GRID_CELL_WIDTH - 1, GRID_CELL_WIDTH - 1))
    pg.display.update()

def backtrack_cell(x, y):
    pg.draw.rect(screen, BLUE, (x + 1, y + 1, GRID_CELL_WIDTH - 1, GRID_CELL_WIDTH - 1))
    pg.display.update()

def carve_out_maze(grid):
    stack = [grid[0]]
    visited = {grid[0]}
    maze = {}
    x, y = grid[0]
    single_cell(x, y)

    while stack:
        sleep(.03)
        neighbors = get_neighbors(x, y, visited, grid)

        if neighbors:
            neighbor = random.choice(neighbors)

            if neighbor == "right":
                push_right(x, y)
                maze[(x + GRID_CELL_WIDTH, y)] = x, y
                x += GRID_CELL_WIDTH
            elif neighbor == "left":
                push_left(x, y)
                maze[(x - GRID_CELL_WIDTH, y)] = x, y
                x -= GRID_CELL_WIDTH
            elif neighbor == "down":
                push_down(x, y)
                maze[(x, y + GRID_CELL_WIDTH)] = x, y
                y += GRID_CELL_WIDTH
            else:
                push_up(x, y)
                maze[(x, y - GRID_CELL_WIDTH)] = x, y
                y -= GRID_CELL_WIDTH

            visited.add((x, y))
            stack.append((x, y))
        else:
            x, y = stack.pop()
            single_cell(x, y)
            sleep(.02)
            backtrack_cell(x, y)

    return maze

def maze_cell(x, y):
    pg.draw.circle(screen, SCARLET, (x + GRID_CELL_WIDTH // 2, y + GRID_CELL_WIDTH // 2), 5)
    pg.display.update()

def solve_maze(maze, x, y):
    maze_cell(x, y)
    while (x, y) != (40, 40):
        x, y = maze[x, y]
        maze_cell(x, y)
        sleep(.1)

def main():
    run = True 
    clock = pg.time.Clock()
    grid = init_grid()
    maze = carve_out_maze(grid)
    solve_maze(maze, 440, 440)

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
                quit()

        clock.tick(FPS)

if __name__ == "__main__":
    main()
