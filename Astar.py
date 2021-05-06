#Import and Initialize Libraries
import sys, pygame, time

pygame.init()

#DEBBUGGER
DEBUG = False

#Colors
BLACK = (0,0,0)
GREY = (148, 143, 143)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (224, 20, 20)
CYAN = (50, 158, 168)
PURPLE = (113, 50, 168)
YELLOW = (222, 230, 71)

#Initialize Window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
WIN.fill(WHITE)
pygame.display.set_caption("A* Pathfinding Algorithm")


#Define Node's

class Node:
    def __init__(self, row, col, width, parent = None):
        self.row = row
        self.col = col
        self.x = row * width
        self.y =  col * width

        self.parent = parent
        self.position = row, col

        self.color = WHITE
        
        self.g = 0
        self.h = 0
        self.f = 0

    def makeStart(self):
        self.color = CYAN 

    def makeGoal(self):
        self.color = PURPLE

    def makeBarrier(self):
        self.color = BLACK

    def makeOpen(self):
        self.color = GREEN

    def makeClosed(self):
        self.color = RED

    def makePath(self):
        self.color = YELLOW

    def clear(self):
        self.color = WHITE

    def isBarrier(self):
        return self.color == BLACK


    def draw(self, width, rows):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, width // rows, width // rows))



#Functional Grid
def makeGrid(width, rows):
    grid = []
    space = width // rows
    for x in range(rows):
        grid.append([])
        for y in range (rows):
            node = Node(x, y, space)
            grid[x].append(node)
    
    return grid


#Draw the grid
def drawGrid(width, rows):
    space = width // rows
    for x in range(0, width, space):
        for y in range(0, width, space):
            pygame.draw.rect(WIN, GREY, (x, y, space, space), 1)


#Get position of clicked node on screen
def getPos(x, y, width, rows):
    col = x // (width / rows)
    row = y // (width / rows)

    return (col, row)


# Calcualate the H score of a given node using Manhattan distance
def calc_h(child, goal):
    x1, y1 = child.position
    x2, y2 = goal.position
    return abs(x1 - x2) + abs (y1 - y2)


#Draw the shortest path between the Start, and Goal Node
def return_path(grid, width, rows, current_node, start):
    current = current_node
    while current.position != start.position:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()

        current.makePath()
        current.draw(width, rows)
        drawGrid(width, rows)
        current = current.parent

        if DEBUG == True:
            time.sleep(3)


#Check if a specfic node is in a given list  
def checklist(node_to_check, list_checked):
    for node in list_checked:
        if node == node_to_check:
            return True
    
    return False
        

#Check if a specigic Node is in a given list, and if it's g-score is lower 
def checklist_and_g(node_to_check, list_checked):
    for node in list_checked:
        if (node == node_to_check) and (node_to_check.g < node.g):
            return True
        
    return False

#The A* algorithm 
def algorithm(grid, width, start, goal, rows):

    # Define Start and End Nodes
    start_node = start
    goal_node = goal

    # Initialize the open and closed lists    
    open_list = []
    closed_list = []
    open_list.append(start_node)

    #List used to check neighbors of current node
    neighbors = [[-1,0],[0,-1],[1,0],[0,1]]  

    while len(open_list) > 0:

        # Allows application to be quit 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        current_node = open_list[0]
        current_index = 0

        children = []

        if DEBUG == True:
            print("looping")

        #Search open list for node with lowest f_score
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        #Move node with lowest f_score to closed list from open list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #Make closed list nodes red for visulization 
        current_node.makeClosed()
        current_node.draw(width, rows)
        drawGrid(width, rows)


        # Draw the shorest path the goal if it is the current node 
        if current_node == goal:
            if DEBUG == True:
                print("DONE")  
            return_path(grid, width, rows, current_node, start)
            break
        
        #Find all children around current_node
        for new_position in neighbors:

            #Get node postion
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            #Check to make sure new node is within maze range
            if (node_position[0] < 0) or (node_position[0] > rows - 1)  or (node_position[1] < 0) or (node_position[1] > rows - 1):
                continue 
            
            #Check to see if new node is on barrier
            temp_x, temp_y = node_position 
            temp_node = grid[temp_x][temp_y]
            if temp_node.color == BLACK:
                continue 

            #Check if new_node is already in the closed list
            if checklist(temp_node, closed_list):
                continue
            
            #Add node to list of children 
            temp_node.parent = current_node
            children.append(temp_node)

        #Loop through children 
        for child in children:
            
            #Check if child is already in closed list   
            if checklist(child, closed_list):
                continue

            # Calculate f_score of child
            child.g = current_node.g + 1
            child.h = calc_h(child, goal)
            child.f = child.g + child.h

            #Check if child is already in the open list AND the g cost is lower
            if checklist_and_g(child, open_list):
                continue

            #Add child to open list
            open_list.append(child)
            #Make open list nodes green for visulization 
            child.makeOpen()
            child.draw(width, rows)
            drawGrid(width, rows)

        children.clear()

        pygame.display.update()

    


#Main Function 
def main(win, width):
    ROWS = 50
    run = True
    space = WIDTH // ROWS

    grid = makeGrid(width, ROWS)
    drawGrid(width, ROWS)
    
    start = None
    goal = None
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:                               #Left Click to PLACE Start, Goal, and Barriers
                x = (event.pos[0] // space) * space
                y = (event.pos[1] // space) * space
                col, row = getPos(x, y, width, ROWS)
                node = grid[int(col)][int(row)]

                if DEBUG == True: 
                    print("x: %d" % col)
                    print("y: %d" % row)
                    print('\n')

                if (start == None) and (node != goal):
                    start = node
                    start.makeStart()
                    start.draw(width,ROWS)
                    drawGrid(width, ROWS)
                elif (goal == None) and (node != start):
                    goal = node
                    goal.makeGoal()
                    goal.draw(width,ROWS)
                    drawGrid(width, ROWS)
                elif (node != start) and (node != goal):
                    node.makeBarrier()
                    node.draw(width, ROWS)
                    drawGrid(width, ROWS)

            if pygame.mouse.get_pressed()[2]:                               #Right click to ERASE Start, Goal, and Barriers 
                x = (event.pos[0] // space) * space
                y = (event.pos[1] // space) * space
                col, row = getPos(x, y, width, ROWS)
                node = grid[int(col)][int(row)]

                if node == start: 
                    start = None
                    node.clear()
                    node.draw(width, ROWS)
                    drawGrid(width, ROWS)
                elif node == goal:
                    goal = None
                    node.clear()
                    node.draw(width, ROWS)
                    drawGrid(width, ROWS)
                else:
                    node.clear()
                    node.draw(width, ROWS)
                    drawGrid(width, ROWS)

            if (start != None) and (goal != None) and (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_RETURN:
                    print("Algorithm Runs")
                    algorithm(grid, width, start, goal, ROWS)               
    

        pygame.display.update()


    if DEBUG == True:
    
        #for x in range(50):  
            #for y in range(50):
                #node = grid[x][y]
                #if node.color == CYAN:
                    #print("Start: %d %d" % node.position)
                #if node.color == YELLOW:
                    #print("Goal: %d %d" % node.position)
                #if node.parent != None:
                    #print(node.parent.position)
                    
        pygame.quit()

main(WIN, WIDTH)

