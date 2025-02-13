# THIS CODE FOR ONE BOT FOR RIGHT AND LEFT MOVEMENT

class Bot:
    def __init__(self, name, start, end):
        self.name = name
        self.position = start
        self.destination = end
        self.commands = []
        self.direction_index = 0  # Starting facing 'up' (0 = Up, 1 = Right, 2 = Down, 3 = Left)

    def move(self, command):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        if command == "forward":
            self.position = (self.position[0] + directions[self.direction_index][0],
                             self.position[1] + directions[self.direction_index][1])
        elif command == "reverse":
            self.position = (self.position[0] - directions[self.direction_index][0],
                             self.position[1] - directions[self.direction_index][1])
        elif command == "left":
            self.direction_index = (self.direction_index - 1) % 4  # Turn left
        elif command == "right":
            self.direction_index = (self.direction_index + 1) % 4  # Turn right
        elif command == "wait":
            pass  # Waiting doesn't change position
        self.commands.append(command)

def is_valid_move(grid, position):
    rows, cols = len(grid), len(grid[0])
    return (0 <= position[0] < rows) and (0 <= position[1] < cols) and (grid[position[0]][position[1]] != 'X')

def get_direction_commands(start_dir_index, end_dir_index):
    commands = []
    clockwise_steps = (end_dir_index - start_dir_index) % 4
    counterclockwise_steps = (start_dir_index - end_dir_index) % 4
    
    if clockwise_steps <= counterclockwise_steps:
        commands.extend(["right"] * clockwise_steps)
    else:
        commands.extend(["left"] * counterclockwise_steps)
    
    return commands

def pathfinding(grid, start, end):
    from collections import deque
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
    
    queue = deque([(start, [], 0)])  # (current position, path, current direction index)
    visited = set()
    visited.add(start)

    while queue:
        current, path, dir_index = queue.popleft()
        if current == end:
            return path
        
        for i in range(4):  # Check all directions
            next_pos = (current[0] + directions[i][0], current[1] + directions[i][1])
            if is_valid_move(grid, next_pos) and next_pos not in visited:
                visited.add(next_pos)
                turn_commands = get_direction_commands(dir_index, i)
                queue.append((next_pos, path + turn_commands + ["forward"], i))
    
    return []

def simulate_movement(bots, grid):
    for bot in bots:
        path = pathfinding(grid, bot.position, bot.destination)
        
        # Execute commands
        for step in path:
            bot.move(step)
        
        print(f"{bot.name}: ({', '.join(bot.commands)})")
        print(f"Final position of {bot.name}: {bot.position}")

def get_custom_input():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    
    print("Enter the grid row by row (use 'A' for starting points, 'B' for destinations, 'X' for obstacles, '.' for free space):")
    grid = [input().strip().split() for _ in range(rows)]
    
    bots = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'A':
                bot_end = find_destination(grid, i, j, rows, cols)
                if bot_end:
                    bots.append(Bot(f"car{len(bots) + 1}", (i, j), bot_end))

    return bots, grid

def find_destination(grid, start_row, start_col, rows, cols):
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'B':
                return (i, j)
    return None

# Main program
if __name__ == "__main__":
    bots, grid = get_custom_input()
    simulate_movement(bots, grid)
