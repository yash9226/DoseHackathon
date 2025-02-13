from collections import deque

class Bot:
    def __init__(self, name, start, end):
        self.name = name
        self.position = start
        self.destination = end
        self.commands = []
        self.direction_index = 0  # Starting facing 'up' (0 = Up, 1 = Right, 2 = Down, 3 = Left)
        self.has_reached_destination = False

    def move(self, command):
        if not self.has_reached_destination:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left (clockwise)
            if command == "forward":
                self.position = (self.position[0] + directions[self.direction_index][0],
                                 self.position[1] + directions[self.direction_index][1])
            elif command == "reverse":
                self.position = (self.position[0] - directions[self.direction_index][0],
                                 self.position[1] - directions[self.direction_index][1])
            elif command == "left":
                self.direction_index = (self.direction_index - 1) % 4
            elif command == "right":
                self.direction_index = (self.direction_index + 1) % 4
            elif command == "wait":
                pass
            
            self.commands.append(command)       
            
            if self.position == self.destination:
                self.has_reached_destination = True

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
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left (clockwise)
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

def simulate_movement(bots, grid, max_commands=25):
    paths = {bot.name: pathfinding(grid, bot.position, bot.destination) for bot in bots}
    max_steps = max(len(path) for path in paths.values())
    
    step = 0
    while step < max_steps:
        if step >= max_commands:
            print(f"Impossible Case Detected: No solution found after {max_commands} commands.")
            return
        
        planned_positions = {}
        for bot in bots:
            if bot.has_reached_destination:
                continue
            
            if step < len(paths[bot.name]):
                next_move = paths[bot.name][step]
                if next_move == "forward":
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    planned_position = (bot.position[0] + directions[bot.direction_index][0],
                                        bot.position[1] + directions[bot.direction_index][1])
                    planned_positions[bot.name] = planned_position
                else:
                    planned_positions[bot.name] = bot.position
            else:
                planned_positions[bot.name] = bot.position

        # Resolve collisions and optimize movement
        for bot in bots:
            if bot.has_reached_destination:
                continue
            
            planned_position = planned_positions[bot.name]
            collision_count = list(planned_positions.values()).count(planned_position)

            if collision_count > 1:  # If there's a collision
                if list(planned_positions.keys()).index(bot.name) == 0:
                    bot.move(paths[bot.name][step])  # First bot moves
                else:
                    bot.move("wait")  # Other bots wait
            else:
                # Move to the next command if not at destination
                if step < len(paths[bot.name]) and bot.position != bot.destination:
                    bot.move(paths[bot.name][step])
                elif bot.position == planned_position:
                    bot.move("wait")  # Wait only if they cannot proceed

        # After all bots attempt to move, check for possible forward moves
        for bot in bots:
            if bot.has_reached_destination:
                continue
            
            # Attempt to move forward if a "wait" was issued previously
            if "wait" in bot.commands and bot.position != bot.destination:
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                forward_position = (bot.position[0] + directions[bot.direction_index][0],
                                    bot.position[1] + directions[bot.direction_index][1])
                if is_valid_move(grid, forward_position):
                    bot.move("forward")  # Move forward if possible

        all_reached = all(bot.has_reached_destination for bot in bots)
        if all_reached:
            break

        step += 1

    # Print bot movements and summary
    total_commands = 0
    max_bot_commands = 0

    for bot in bots:
        bot_commands = len(bot.commands)
        print(f"{bot.name}: {bot_commands} commands ({', '.join(bot.commands)})")
        total_commands += bot_commands
        max_bot_commands = max(max_bot_commands, bot_commands)

    average_commands = total_commands / len(bots) if bots else 0
    print(f"Average Commands: {average_commands:.2f} commands.")
    print(f"Maximum Commands: {max_bot_commands} commands.")

def get_custom_input():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    
    print("Enter the grid row by row (use 'A1', 'A2', ... for starting points, 'B1', 'B2', ... for destinations, 'X' for obstacles, '.' for free space):")
    grid = [input().strip().split() for _ in range(rows)]
    
    bots = []
    start_positions = {}
    end_positions = {}

    for i in range(rows):
        for j in range(cols):
            if grid[i][j].startswith('A'):
                start_positions[grid[i][j]] = (i, j)
            elif grid[i][j].startswith('B'):
                end_positions[grid[i][j]] = (i, j)
    
    for start_label, start_pos in start_positions.items():
        bot_number = start_label[1:]  # Extract bot number from 'A1', 'A2', etc.
        end_label = f'B{bot_number}'  # Match with corresponding 'B1', 'B2', etc.
        if end_label in end_positions:
            bots.append(Bot(f"Bot{bot_number}", start_pos, end_positions[end_label]))

    return bots, grid

# Main program
if __name__ == "__main__":
    bots, grid = get_custom_input()
    simulate_movement(bots, grid)