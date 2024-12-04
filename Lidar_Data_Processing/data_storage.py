from math import cos, sin
from search import find_search_point, path_planning, search

# ALL MEASUREMENTS ARE IN CENTIMETERS

MAX = 5000          # Dimensions for 2D array that stores the robot's perceived world
start_X = 457       # Starting X position of the robot
start_Y = 457       # Starting Y position of the robot
robot_X = 457       # Current X position of the robot
robot_Y = 457       # Current Y position of the robot
robot_rad = 16      # Radius of the robot
min_X = 0           # Minimum X position seen by the robot
max_X = 0           # Max X position seen by the robot
min_Y = 0           # Minimum Y position seen by the robot
max_Y = 0           # Max Y position seen by the robot
target_X = 0
target_Y = 0
orientation = 0

# Initialized with the char 'U' as unvisited
global_map = [['U' for i in range(MAX)] for y in range(MAX)]

# Used to update the robot's position
def update_robot_position(new_X, new_Y, new_Orient):
    robot_X = new_X
    robot_Y = new_X
    orientation = new_Orient
    min_X = MAX + 1
    max_X = 0
    min_Y = MAX + 1

def insert_target(angle, distance):
    dist_X = distance * cos(angle - orientation)
    dist_Y = distance * sin(angle - orientation)
    target_X = robot_X + dist_X
    target_Y = robot_Y + dist_Y

    global_map[target_X][target_Y] = 'T'

# Sends the path for moving the robot implemented in the search.py file
def output_data(str):
    # calculate path if cup is found and returning to starting position
    if str == "Received":
        tmp = search(global_map, start_X, start_Y, robot_X, robot_Y, MAX)
        res = tmp[0:-3]
        res.reverse()
        res.append(orientation)
        update_robot_position(tmp[-2], tmp[-1], tmp[-3])
    # calculate path to cup 
    elif str == "Target":
        tmp = search(global_map, robot_X, robot_Y, target_X, target_Y, MAX)
        res = tmp[0:-3]
        res.append(orientation)
        update_robot_position(tmp[-2], tmp[-1], tmp[-3])
    # still searching
    else:
        tmp = search(global_map, robot_X, robot_Y, -1, -1, MAX)
        res = tmp[0:-3]
        res.append(orientation)
        update_robot_position(tmp[-2], tmp[-1], tmp[-3])
        
    return res

# Insert lidar data into the global map
def insert_data(angle, distance):
    dist_X = distance * cos(angle)
    dist_Y = distance * sin(angle)

    # Record the max and min X and Y positions seen by the lidar
    if robot_X + dist_X < min_X:
        min_X = robot_X + dist_X
    if robot_X + dist_X > max_X:
        max_X = robot_X + dist_X
    if robot_Y + dist_Y < min_Y:
        min_Y = robot_Y + dist_Y
    if robot_Y + dist_Y > max_Y:
        max_Y = robot_Y + dist_Y

    global_map[robot_X + dist_X][robot_Y + dist_Y] = '|'

# Fills in the map with 'X' extending from the walls (char '|') to ensure
# the robot will fit through the calculated path
def fill():
    for x in range(min_X, max_Y):
        for y in range(min_Y, max_Y):
            if global_map[x][y] == '|':
                if x+1 < max_X and global_map[x+1][y] == 'U':
                    for z in range(robot_rad+1):
                        if x+z < max_X and global_map[x+z][y] != '|':
                            global_map[x+z][y] = 'X'
                            
                if y+1 < max_Y and global_map[x][y+1] == 'U':
                    for z in range(robot_rad+1):
                        if y+z < max_Y  and global_map[x][y+z] != '|':
                            global_map[x][y+z] = 'X'
                
                if x > min_X and global_map[x-1][y] == 'U':
                    for z in range(robot_rad+1):
                        if x-z >= min_X and global_map[x-z][y] != '|':
                            global_map[x-z][y] = 'X'
                            
                if y > min_Y and global_map[x][y-1] == 'U':
                    for z in range(robot_rad+1):
                        if y-z >= min_Y and global_map[x][y-z] != '|':
                            global_map[x][y-z] = 'X'

                if x > min_X and y > min_Y and global_map[x-1][y-1] == 'U':
                    global_map[x-1][y-1] = 'X'

                if x+1 < max_X and y+1 < max_Y and global_map[x+1][y+1] == 'U':
                    global_map[x+1][y+1] = 'X'

                if x > min_X and y+1 < max_Y and global_map[x-1][y+1] == 'U':
                    global_map[x-1][y+1] = 'X'

                if x+1 < max_X and y > min_Y and global_map[x+1][y-1] == 'U':
                    global_map[x+1][y-1] = 'X'

    # fill in remaining spaces with the char 'O' for open (robot can move through this point)
    for x in range(min_X, max_X):
        for y in range(min_X, min_Y):
            if global_map[x][y] == 'U':
                global_map[x][y] = 'O'