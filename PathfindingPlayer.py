from collections import deque

def bfs(start, goal, grid, walls):
  """
  Performs Breadth-First Search to find a path from start to goal on a grid.

  Args:
    start: Starting position (tuple of (row, col)).
    goal: Goal position (tuple of (row, col)).
    grid: A 5x5 list of lists representing the grid. 1 indicates an obstacle, 0 is free.

  Returns:
    A list of tuples representing the path from start to goal, or None if no path exists.
  """

  queue = deque([(start, [])])
  visited = set()

  while queue:
    (node, path) = queue.popleft()
    if node == goal:
      return path + [goal]
    if node not in visited:
      visited.add(node)
      for neighbor in get_neighbors(node, grid):
        if neighbor not in visited:
          queue.append((neighbor, path + [node]))
  return None

def get_neighbors(node, grid): #Returns valid neighbors of a node on the grid.
  neighbors = []
  row, col = node
  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    r, c = row + dr, col + dc
    if 0 <= r < 5 and 0 <= c < 5 and grid[r][c] == 0:
        if not is_blocked_by_wall((row, col), (r, c), walls):
            neighbors.append((r, c))
  return neighbors

def is_blocked_by_wall(start, end, walls):
  #Wall at (row, col) blocks movement from (row, col) to (row+1, col) or (row, col) to (row, col+1)
  sx, sy = start
  ex, ey = end
  if ex - sx == 1: #Horizontal movement
    return ('h', sx, sy) in walls
  elif ey - sy == 1: #Vertical movement
    return ('v', sx, sy) in walls
  else:
    return False


grid = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]

walls = [('h',0,0),('v',0,1)] #Wall structure : (v/h,x,y) where wall orientation is indicated by 'v' or 'h'

start = (0, 0) #There we just retrieve the player position
goal = (4, 4) #We need to just this to be a specific line not a specific square

path = bfs(start, goal, grid, walls)
if path:
  print(path)
  #len(path) will help to choose the best path to win as they are several valid squares to win
else:
  print("No path found") #Impossible as it would be due to a forbidden move played prior

