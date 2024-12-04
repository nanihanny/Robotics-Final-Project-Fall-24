# Finds the start position 'S' and end position 'E'
def find_start_and_end(grid):
    start, end = None, None
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'S':
                start = (x, y)
            elif grid[x][y] == 'E':
                end = (x, y)
    return start, end

# finds a path from the start position to the end position
def dfs(grid, x, y, visited, path_x, path_y):
    # Check bounds and if cell is valid to visit
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]) or grid[x][y] in ['|', 'X'] or (x, y) in visited:
        return False

    # Add current cell to visited set and path
    visited.add((x, y))
    path_x.append(x)
    path_y.append(y)

    # If endpoint 'E' is found, return True
    if grid[x][y] == 'E':
        return True

    # Define possible moves: up, down, left, right
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in directions:
        if dfs(grid, x + dx, y + dy, visited, path_x, path_y):
            return True

    # Backtrack: Remove the cell from the path if no solution is found in this branch
    path_x.pop()
    path_y.pop()
    return False

# Fills in the map with path for robot
def update_map_with_path(global_map, path_x, path_y):
    for i in range(1,len(path_x)-1):
        global_map[path_x[i]][path_y[i]] = '*'

# Delete the path in map
def delete_path(global_map, path_x, path_y):
    for i in range(1,len(path_x)-1):
        global_map[path_x[i]][path_y[i]] = 'O'

# Given the path creating by the dfs, calculate when to turn and distance traveled
# For turning: 1 -> right, -1 -> left, 0 -> do nothing
orient = 0
def path_planning(path_x, path_y, orient):
    # return array
    res = []

    # i -> index, orient -> orientation, distance -> distance traveled before turning
    i = 0
    distance = 0
    if i < len(path_x)-1 and path_x[i] == path_x[i+1]:
        if orient == 90 and path_y[i+1] - path_y[i] > 0:
            res.append(-90)
        elif orient == 90 and path_y[i+1] + path_y[i] < 0:
            res.append(90)

        elif orient == -90 and path_y[i+1] - path_y[i] > 0:
            res.append(90)
        elif orient == -90 and path_y[i+1] + path_y[i] < 0:
            res.append(-90)
        else:
            res.append(0)

    elif i < len(path_y)-1 and path_y[i] == path_y[i+1]:
        if orient == 0 and path_x[i+1] - path_x[i] > 0:
            res.append(90)
        elif orient == 0 and path_x[i+1] + path_x[i] < 0:
            res.append(-90)

        elif orient == 180 and path_x[i+1] - path_x[i] > 0:
            res.append(-90)
        elif orient == 180 and path_x[i+1] + path_x[i] < 0:
            res.append(90)
        else:
            res.append(0)
    

    # create data for return array
    while i < len(path_x):
        distance = 0

        # Follow the line of the path until a turn is required
        if(i < len(path_x)-1 and path_x[i] == path_x[i+1]):            
            # iterate through path until turn is found
            while i < len(path_x)-1 and path_x[i] == path_x[i+1]:
                i += 1
                distance += 1
        
            # record direction of turn
            if i < len(path_x) - 1:
                print("X: {}, {}, {}" .format(path_x[i], path_x[i+1], i))
                if path_x[i+1] - path_x[i] > 0 and orient == 0:
                    res.append(90)
                    orient += 90
                elif path_x[i+1] - path_x[i] < 0 and orient == 0:
                    res.append(-90)
                    orient -= 90
                elif path_x[i+1] - path_x[i] > 0 and orient == 180:
                    res.append(-90)
                    orient -= 90
                elif path_x[i+1] - path_x[i] < 0 and orient == 180:
                    res.append(90)
                    orient += 90

        else:
            # iterate through path until turn is found
            while i < len(path_y) - 1 and path_y[i] == path_y[i+1]:
                i += 1
                distance += 1
        
            # record direction of turn
            if i < len(path_x) - 1:
                print("Y: {}, {}" .format(path_y[i], path_y[i+1]))

                if path_y[i+1] - path_y[i] < 0 and orient == 90:
                    res.append(90)
                    orient += 90
                elif path_y[i+1] - path_y[i] > 0 and orient == 90:
                    res.append(-90)
                    orient -= 90
                elif path_y[i+1] - path_y[i] < 0 and orient == -90:
                    res.append(-90)
                    orient -= 90
                elif path_y[i+1] - path_y[i] > 0 and orient == -90:
                    res.append(90)
                    orient += 90

        # record distance traveled before turn     
        res.append(distance + 1)

        # iterate to next position
        i += 1     

    # return path_planning array
    res.append(orient)
    return res

# Finds the position where the map changes from Open ('O') to Unvisited ('U')   
def find_search_point(global_map, max):
    for x in range(max):
        for y in range(max):
            if global_map[x][y] == 'O':
                if x + 1 < max and global_map[x+1][y] == 'U':
                    global_map[x+1][y] = 'E'
                    return [x+1, y]
                if x - 1 > -1 and global_map[x-1][y] == 'U':
                    global_map[x-1][y] = 'E'
                    return
                if y + 1 < max and global_map[x][y+1] == 'U':
                    global_map[x][y + 1] = 'E'
                    return
                if y - 1 > -1 and global_map[x][y-1] == 'U':
                    global_map[x+1][y - 1] = 'E'
                    return

# Calculated the path from start to end and returns directions on how 
# to move from start to end position               
def search(global_map, start_x, start_y, end_x, end_y, max):
    # Initialize DFS
    start = (start_x, start_y)
    global_map[start_x][start_y] = 'S'
    if end_x == -1:
        end = find_search_point(global_map, max)
    else:
        global_map[end_x][end_y] = 'E'
    
    # declare variables
    visited = set()
    path_x = []
    path_y = []
    orient = 0
    if dfs(global_map, start[0], start[1], visited, path_x, path_y):
        print("Path found!")
        update_map_with_path(global_map, path_x, path_y)

        # calculate path
        path = path_planning(path_x, path_y, orient)

        # print map
        for row in global_map:
            print(*row)
        
        # convert map back to original self
        global_map[start_x][start_y] = 'O'
        global_map[end_x][end_y] = 'U'
        delete_path(global_map, path_x, path_y)

        path.append(end[0])
        path.append(end[1])

        return path
    else:
        print("No path found.")