from collections import deque

def bfs(start, goals, grid, walls):
  """
  Performs Breadth-First Search to find a path from start to goal on a grid.

  Args:
    start: Starting position (tuple of (row, col)).
    goal: Goal position (tuple of (row, col)).
    grid: A 5x5 list of lists representing the grid. 1 indicates an obstacle, 0 is free.

  Returns:
    A list of tuples representing the path from start to goal, or None if no path exists.
  """
  paths = []

  for goal in goals:
    queue = deque([(start, [])])
    visited = set()

    while queue:
      (node, path) = queue.popleft()
      if node == goal:
        paths.append(path + [goal])
      if node not in visited:
        visited.add(node)
        for neighbor in get_neighbors(node, grid, walls):
          if neighbor not in visited:
            queue.append((neighbor, path + [node]))
  if len(paths) == 0:
    return None
  else:
    shortest = 0
    for i in range(len(paths)):
      if len(paths[i]) < len(paths[shortest]):
        shortest = i
    return paths[shortest]


def get_neighbors(node, grid, walls): #Returns valid neighbors of a node on the grid.
  neighbors = []
  row, col = node
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    r, c = row + dr, col + dc
    if 0 <= r < 5 and 0 <= c < 5 and grid[r][c] == 0:
        if not is_blocked_by_wall((row, col), (r, c), walls):
            neighbors.append((r, c))
  return neighbors

def is_blocked_by_wall(start, end, walls):
  sy, sx = start
  ey, ex = end
  x_min = min(sx,ex)
  y_min = min(sy,ey)
  if ex - sx == 1 or ex - sx == -1: #Vertical movement
    return ('V', y_min, x_min) in walls
  elif ey - sy == 1 or ey - sy == -1: #Horizontal movement
    return ('H', y_min, x_min) in walls
  else:
    return False

def input_to_reach_next(actual,next):
  move = (next[0]-actual[0],next[1]-actual[1])
  if move == (-1,0):
    return 'U'
  elif move == (1,0):
    return 'D'
  elif move == (0,-1):
    return 'L'
  elif move == (0,1):
    return 'R'
  else:
    return "Error"

def transformBoardToWallsTuple(board):
        wallsTuple = []
        for y in range(5):
            for x in range(5):
                if board[y][x] != False:
                    if board[y][x] == 'HH' or board[y][x] == 'H':
                      wallsTuple.append(('H',y,x))
                    elif board[y][x] == 'VV' or board[y][x] == 'V':
                      wallsTuple.append(('V',y,x))
                    elif board[y][x] == 'HV':
                      wallsTuple.append(('V',y,x))
                      wallsTuple.append(('H',y,x))
        return wallsTuple


#wallfunc
def place_wall(self, game, wall_type, row, col):
    """
    Attempt to place a wall for Player 1.
    return:
    bool: True if wall placed
    """
    # check walls left
    if game.walls['P1'] <= 0:
        return False
    
    # check coordo in valid range
    if row < 0 or row >= game.board_size - 1 or col < 0 or col >= game.board_size - 1:
        return False
    
    # if wall isn't offboard
    if (wall_type == 'H' and col == game.board_size - 2) or (wall_type == 'V' and row == game.board_size - 2):
        return False
    
    # if space taken by a wall
    if game.board[row][col] != False or game.board[row][col+1] != False or game.board[row+1][col] != False:
        return False
    
    # place it temp
    previous = game.update_board_wall((wall_type, row, col))
    
    # check if p1 and p2 can reach
    p1_can_reach = game.reachable(game.player_positions['P1'], (0, 0))
    p2_can_reach = game.reachable(game.player_positions['P2'], (game.board_size-1, 0))
    
    if not (p1_can_reach and p2_can_reach):
        # revert cuz those dumasses cannot reach
        game.restore_board_wall((wall_type, row, col), previous)
        return False
    
    # valid placement
    return True




# # TEST

# grid = [
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0]
# ]

# walls = [('V',1,1),('H',0,2),('H',1,2)] #Wall structure : (v/h,y,x) where wall orientation is indicated by 'v' or 'h'

# start = (1,2) #There we just retrieve the player position
# goals = [(2,1)] #We need to just this to be a specific line not a specific square

# path = bfs(start, goals, grid, walls)
# if path:
#   # print(path)
#   # print(input_to_reach_next(path[0],path[1]))
#   #len(path) will help to choose the best path to win as they are several valid squares to win
# else:
#   # print("No path found") #Impossible as it would be due to a forbidden move played prior

