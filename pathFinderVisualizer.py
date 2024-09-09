import pygame
import sys

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 50

box_width = window_width // columns
box_height = window_height // rows

grid = []

class Box: #this is a node object, basically the little squares that make up the grid. It will be interactive

    def __init__(self, i, j): # i, j is for positioning the little boxes, __init__ just means constructor
        self.x = i 
        self.y = j
        self.start = False #start, wall, target means the state of a node. A node can either be untouched, source, target or wall
        self.wall = False
        self.target = False

    def draw(self, win, color):  # this draw function will help print our grid
        pygame.draw.rect(win, color, (self.x * box_width,
                         self.y * box_height, box_width-2, box_height-2))    


for i in range(columns): # we are STORING our boxes in the grid in the form of a 2d array.
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)      

def main():

    start_box_set = False #checking for source node
    target_box_set = False #checking for target node

    while True:
            for event in pygame.event.get(): #checking for events, like mouse movement, closing the window

                # Quit Window
                if event.type == pygame.QUIT:
                    pygame.quit()      
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height    

                    if (pygame.mouse.get_pressed()[2]) and not target_box_set:
                        target_box = grid[i][j]
                        target_box.target = True
                        target_box_set = True 

                    if (pygame.mouse.get_pressed()[0]):  # Left mouse button click

                        if not start_box_set and not grid[i][j].wall:
                            start_box = grid[i][j]
                            start_box.start = True
                            start_box_set = True

                elif event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                # Draw Wall
                    if event.buttons[0]:
                        i = x // box_width
                        j = y // box_height

                        if (not grid[i][j].start):
                            grid[i][j].wall = True
                  
                     
            window.fill((0, 0, 0))

            for i in range(columns): #drawing the grid
                for j in range(rows):
                    box = grid[i][j]                   
                    box.draw(window, (50, 50, 50))  #this will draw the grid

                    if box.start: #finally drawing our boxes
                        box.draw(window, (0, 255, 0)) 
                    if box.wall:
                        box.draw(window, (10, 10, 10))
                    if box.target:
                        box.draw(window, (255, 0, 0))


            pygame.display.flip()    
main() 
