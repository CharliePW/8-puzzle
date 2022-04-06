import time

# Node class, there will be 9 of these in the 8-puzzle
class Node:

    def __init__(self, puzzle, parent):
        """ 
        Constructor for the Node.
        The attributes are: the matrix, the child level and the node's f value.
        """
        self.puzzle = puzzle
        self.parent = parent
        self.depth = 0
        self.h_val = 0
        self.f_val = 0


    def __eq__(self,other):
        return self.puzzle == other.puzzle



def getChildren(node):
    """
    Generates the next possible nodes to search
    """
    puz = node.puzzle
    
    # get the coords of the 0
    x,y = getCoords(puz, "0")

    children = []

    # up swap
    if y+1 < 3:
        child = copy(puz)
        child[x][y] = child[x][y+1]
        child[x][y+1] = "0"
        children.append(Node(child, node))

    # down swap
    if y-1 >= 0:
        child = copy(puz)
        child[x][y] = child[x][y-1]
        child[x][y-1] = "0"
        children.append(Node(child, node))

    # left swap
    if x-1 >= 0:
        child = copy(puz)
        child[x][y] = child[x-1][y]
        child[x-1][y] = "0"
        children.append(Node(child, node))

    # right swap
    if x+1 < 3:
        child = copy(puz)
        child[x][y] = child[x+1][y]
        child[x+1][y] = "0"
        children.append(Node(child, node))

    return children


def getCoords(puz, num):
    """
    Finds the coords of the empty (or zero) value
    """
    # iterate through the rows
    for i in range(3):
        # iterate through the items
        for j in range(3):
            # if the item is the 0
            if puz[i][j] == num:
                # return its coords
                return i,j


def copy(puz):
        """
        Copies the puzzle for the swapping
        """
        new_puz = []
        # iterate through the 2D array puzzle
        for row in puz:
            line = []
            for item in row:
                # add items to the row
                line.append(item)
            # add rows to the new matrix
            new_puz.append(line)
        # return the copy
        return new_puz


def make_matrix(puz):
        """
        takes the array of values and makes it a 2D array
        """
        # the 2D puzzle to be returned
        matrix = [[],[],[]]

        # iterate through the list
        for i in range(len(puz)):
            # if it's the first 3, add the the 1st row
            if i<=2:
                matrix[0].append(puz[i])
            # the next 3 add to the 2nd row
            elif i>2 and i<=5:
                matrix[1].append(puz[i])
            # the last 3 add to the 3rd row
            elif i>5:
                matrix[2].append(puz[i])
            # otherwise there's an error
            else:
                print("Index Error.")
        return matrix
        

def manhattan(start, goal):
        """
        Heursitic Function -
        Returns the distance between the start and goal state
        """
        distance = 0
        for x1 in range(3):
            for y1 in range(3):
                char = start[x1][y1]
                x2, y2 = getCoords(goal, char)
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance


def difference(start, goal):
    """
    Heuristic function - 
    Returns the difference between the start and goal states
    """
    h = 0
    # iterate through the 2D array
    for i in range(3):
        for j in range(3):
            # if the items are different
            if start[i][j] != goal[i][j]:
                # if the start item isn't the empty value
                if start[i][j] != "0":
                    # increment the difference
                    h += 1
    return h

def display_matrix(puz):
    """
    To display the 2D array as a matrix
    """
    str = ""
    for i in range(3):
        str += "\n"
        for j in range(3):
            str += puz[i][j]
            str += " "
    str += "\n"
    print(str)


def getBestNode(openList):
    """
    get the best node available among nodes
    """

    first = True
    for node in openList:
        if first or node.f_val < bestF:
            first = False
            bestNode = node
            bestF = bestNode.f_val
    return bestNode

def search(start,goal, isMan):
    """
    This function contains the A* search functionality
    """

    openList = []
    closedList = []
    openList.append(start)

    while openList:
        
        # get the best node
        current = getBestNode(openList)

        # if it's the goal
        if current.puzzle == goal:
            return current

        # add to the closed list
        openList.remove(current)
        closedList.append(current)

        # expand the node
        for child in getChildren(current):

            # if child in closedList
            inClosed = False   
            for node in closedList:
                if node == child:
                    inClosed = True
                    break

            # if child not in closed list
            if not inClosed:              
                g_val = current.depth + 1 
                inOpen = False

                # if child in open list
                i = 0
                for i in range(len(openList)):
                    node = openList[i]
                    if node == child:
                        inOpen = True
                        # validate child
                        if g_val < node.depth:
                            # add the properties
                            node.depth = g_val
                            node.f_val = node.depth + node.h_val
                            node.parent = current

                # if child not in open list
                if not inOpen:
                    # add the properties
                    child.depth = g_val

                    child.h_val = 0
                    if isMan == True:
                        child.h_val = manhattan(child.puzzle, goal)
                    elif isMan == False:
                        child.h_val = difference(child.puzzle, goal)

                    child.f_val = child.depth + child.h_val
                    child.parent = current
                    openList.append(child)

    return None

def main():
    """
    The main function of the game.
    This contains all the functionality of the game.
    """
    print("Would you like to implement the Manhattan distances or Euclidean?")
    print("Y for Euclidean, N for Manhattan")
    heuristic = input()
    while heuristic != "Y" and heuristic != "N":
        print("Y for misplaced tiles, N for manhattan")
        heuristic = input()

    # input the start values
    print("Enter the start puzzle: ")
    start = input().split(" ")
    start = make_matrix(start)
    display_matrix(start)

    # input the goal values
    print("Enter the goal puzzle: ")
    goal = input().split(" ")
    goal = make_matrix(goal)
    display_matrix(goal)
    
    # turn start matrix into node
    startNode = Node(start,None)

    result = None
    
    # type of heuristic and timer
    t0 = time.time()
    if heuristic == "Y":
        result = search(startNode,goal, False)
    elif heuristic == "N":
        result = search(startNode,goal, True)
    t1 = time.time()

    print("Time:" + str(t1-t0))
    path = []
    total = 0

    # getting the length of the path
    if(not result):
        print ("No solution")
    else:
        print(result.puzzle)
        t=result.parent
        while t:
            total += 1
            print(t.puzzle)
            t=t.parent
    print("Length of path: " + str(total))
    

if __name__ == "__main__":
    main()
    