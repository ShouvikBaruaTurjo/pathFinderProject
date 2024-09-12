from tkinter import messagebox, Tk
import pygame
import sys
import heapq  # for priority queue

class PathfindingApp:
    def __init__(self):
        # Initialize Pygame and set up the window
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window_width = 800
        self.window_height = 800
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        # Initialize grid
        self.columns = 50
        self.rows = 50
        self.box_width = self.window_width // self.columns
        self.box_height = self.window_height // self.rows
        self.grid = [[Box(i, j, self) for j in range(self.rows)] for i in range(self.columns)]
        self.queue = []
        self.stack = []
        self.open_set = []
        self.path = []
        self.searching = True
        self.current_algorithm = Algorithm.DIJKSTRA
        self.start_box = None
        self.target_box = None
        self.begin_search = False
        self.started = False

        # Set neighbors for each box in the grid
        for row in self.grid:
            for box in row:
                box.set_neighbours()

    def heuristic(self, a, b):
        # Using Manhattan distance as the heuristic
        if a is None or b is None:  # Prevent NoneType access
            return float('inf')
        return abs(a.x - b.x) + abs(a.y - b.y)

    def reconstruct_path(self, current_box):
        while current_box.previous:
            current_box = current_box.previous
            current_box.visited = True

    def dijkstra(self):
        if self.begin_search and self.searching and self.target_box and self.start_box:
            if self.queue:
                current_box = self.queue.pop(0)
                current_box.visited = True
                if current_box == self.target_box:
                    self.searching = False
                    while current_box.previous != self.start_box:
                        self.path.append(current_box.previous)
                        current_box = current_box.previous
                    Tk().wm_withdraw()
                    messagebox.showinfo("Solution Found", "Target has been found!")
                    return
                for neighbour in current_box.neighbours:
                    if not neighbour.queued and not neighbour.wall:
                        neighbour.queued = True
                        neighbour.previous = current_box
                        self.queue.append(neighbour)
            else:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def bfs(self):
        if self.begin_search and self.searching and self.target_box and self.start_box:
            if self.queue:
                current_box = self.queue.pop(0)
                current_box.visited = True
                if current_box == self.target_box:
                    self.searching = False
                    while current_box.previous != self.start_box:
                        self.path.append(current_box.previous)
                        current_box = current_box.previous
                    Tk().wm_withdraw()
                    messagebox.showinfo("Solution Found", "Target has been found!")
                    return
                for neighbour in current_box.neighbours:
                    if not neighbour.queued and not neighbour.wall:
                        neighbour.queued = True
                        neighbour.previous = current_box
                        self.queue.append(neighbour)
            else:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def dfs(self):
        if self.begin_search and self.searching and self.target_box and self.start_box:
            if self.stack:
                current_box = self.stack.pop()
                current_box.visited = True
                if current_box == self.target_box:
                    self.searching = False
                    while current_box.previous != self.start_box:
                        self.path.append(current_box.previous)
                        current_box = current_box.previous
                    Tk().wm_withdraw()
                    messagebox.showinfo("Solution Found", "Target has been found!")
                    return
                for neighbour in current_box.neighbours:
                    if not neighbour.queued and not neighbour.wall:
                        neighbour.queued = True
                        neighbour.previous = current_box
                        self.stack.append(neighbour)
            else:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def a_star(self):
        if self.begin_search and self.searching and self.target_box and self.start_box:
            if self.open_set:
                current_box = heapq.heappop(self.open_set)
                current_box.visited = True
                if current_box == self.target_box:
                    self.reconstruct_path(current_box)
                    self.searching = False
                    while current_box.previous != self.start_box:
                        self.path.append(current_box.previous)
                        current_box = current_box.previous
                    Tk().wm_withdraw()
                    messagebox.showinfo("Solution Found", "Target has been found!")
                    return
                for neighbour in current_box.neighbours:
                    if not neighbour.visited and not neighbour.wall:
                        neighbour.previous = current_box
                        tentative_g = current_box.g + 1
                        if tentative_g < neighbour.g:
                            neighbour.g = tentative_g
                            neighbour.f = neighbour.g + self.heuristic(neighbour, self.target_box)
                            neighbour.previous = current_box
                            if neighbour not in self.open_set:
                                heapq.heappush(self.open_set, neighbour)
            else:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                self.searching = False

    def reset_grid(self):
        for row in self.grid:
            for box in row:
                box.reset()
        self.queue = []
        self.stack = []
        self.open_set = []
        self.path = []
        self.start_box = None
        self.target_box = None
        self.searching = True
        self.begin_search = False
        self.started = False

    def main(self):
        maze_drawing = False  # Flag to track if we're drawing the maze
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    i = x // self.box_width
                    j = y // self.box_height

                    if pygame.mouse.get_pressed()[2] and not self.target_box:
                        self.target_box = self.grid[i][j]
                        self.target_box.target = True

                    if pygame.mouse.get_pressed()[0]:
                        if not self.start_box and not self.grid[i][j].wall:
                            self.start_box = self.grid[i][j]
                            self.start_box.start = True
                            self.start_box.visited = True
                            self.queue.append(self.start_box)
                            self.stack.append(self.start_box)
                            self.start_box.g = 0
                            self.start_box.f = self.heuristic(self.start_box, self.target_box)
                            heapq.heappush(self.open_set, self.start_box)
                            self.started = True
                        maze_drawing = True  # Start drawing maze

                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pressed()[0] == 0:
                        maze_drawing = False  # Stop drawing maze

                elif event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    i = x // self.box_width
                    j = y // self.box_height
                    if maze_drawing:
                        if not self.grid[i][j].start and not self.grid[i][j].target:
                            self.grid[i][j].wall = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press 'R' to reset
                        self.reset_grid()
                    elif event.key == pygame.K_1 and self.target_box and self.start_box:  # Press '1' for Dijkstra
                        self.current_algorithm = Algorithm.DIJKSTRA
                    elif event.key == pygame.K_2 and self.target_box and self.start_box:  # Press '2' for BFS
                        self.current_algorithm = Algorithm.BFS
                    elif event.key == pygame.K_3 and self.target_box and self.start_box:  # Press '3' for DFS
                        self.current_algorithm = Algorithm.DFS
                    elif event.key == pygame.K_4 and self.target_box and self.start_box:  # Press '4' for A*
                        self.current_algorithm = Algorithm.A_STAR

                    if self.target_box and self.start_box:
                        self.begin_search = True
                        self.started = True

            if self.searching:
                if self.current_algorithm == Algorithm.DIJKSTRA:
                    self.dijkstra()
                elif self.current_algorithm == Algorithm.BFS:
                    self.bfs()
                elif self.current_algorithm == Algorithm.DFS:
                    self.dfs()
                elif self.current_algorithm == Algorithm.A_STAR:
                    self.a_star()

            self.window.fill((0, 0, 0))

            for row in self.grid:
                for box in row:
                    box.draw(self.window)

            self.clock.tick(60)
            pygame.display.flip()



class Box:
    def __init__(self, i, j, app):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.g = float('inf')
        self.f = float('inf')
        self.previous = None
        self.prior = None
        self.app = app  # Reference to the PathfindingApp instance

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(self.app.grid[self.x - 1][self.y])
        if self.x < len(self.app.grid) - 1:
            self.neighbours.append(self.app.grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(self.app.grid[self.x][self.y - 1])
        if self.y < len(self.app.grid[0]) - 1:
            self.neighbours.append(self.app.grid[self.x][self.y + 1])

    def draw(self, win):
        color = (50, 50, 50)  # Default color
        if self.queued:
            color = (255, 255, 0)  # Yellow (queued)
        if self.visited:
            color = (0, 0, 255)  # Blue (visited)
        if self in self.app.path:
            color = (255, 255, 255)  # White (path)
        if self.start:
            color = (0, 255, 0)  # Green (start)
        if self.wall:
            color = (10, 10, 10)  # Dark gray (wall)
        if self.target:
            color = (255, 0, 0)  # Red (target)
        
        pygame.draw.rect(win, color, (self.x * self.app.box_width, self.y * self.app.box_height, self.app.box_width - 2, self.app.box_height - 2))

    def reset(self):
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.g = float('inf')
        self.f = float('inf')
        self.previous = None
        self.prior = None

    def __lt__(self, other):
        return self.f < other.f

class Algorithm:
    DIJKSTRA = 0
    DFS = 1
    BFS = 2
    A_STAR = 3

if __name__ == "__main__":
    app = PathfindingApp()
    app.main()
