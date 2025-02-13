# Code Crafters
# Multi-Bot Grid Navigation Simulator

This project simulates the movement of multiple autonomous bots within a grid. Each bot must navigate from a designated starting point to a destination while avoiding obstacles and potential collisions with other bots. The simulation uses pathfinding algorithms to control and coordinate the bots' movements.


## Overview

The **Multi-Bot Grid Navigation Simulator** is a Python simulation where multiple bots navigate on a grid from start to destination points, avoiding collisions and obstacles. Bots move based on a set of commands (`forward`, `left`, `right`, `wait`) and employ a Breadth-First Search (BFS) algorithm for pathfinding.


## Features

- **Multiple Bot Navigation**: Multiple bots moving simultaneously on a grid with collision avoidance.
- **Pathfinding**: Uses the BFS algorithm to determine the shortest path for each bot.
- **Command System**: Bots receive and execute a sequence of movement commands (`forward`, `left`, `right`, `wait`).
- **Collision Detection**: Bots will pause or reroute if a collision is detected with another bot.
- **Custom Grid Layout**: Supports user-defined grid size, start positions, destinations, and obstacles.


## How It Works

### Pathfinding
Bots use a **breadth-first search (BFS)** algorithm to find the shortest, obstacle-free path to their destination. BFS systematically explores all possible routes, ensuring the bots take the most efficient path available.

### Movement Commands
Bots are issued a set of simple movement commands:
- **forward**: Move one step forward in the current direction.
- **right**: Turn 90 degrees to the right.
- **left**: Turn 90 degrees to the left.
- **wait**: Stay in the current position, typically used to prevent collisions.

### Collision Avoidance
If two or more bots are about to collide, the system detects the potential collision and issues `wait` commands to the appropriate bots, ensuring they wait for the path to clear before moving.


## Customization

You can modify the grid layout, bot start and destination positions, and obstacle locations by providing input during the simulation setup.

### Modifying the Grid
At the start of the simulation, you will be prompted to define the grid structure. You can customize the grid as follows:

- **Grid Size**: Specify the number of rows and columns for the grid.
- **Starting Points**: Mark bot starting positions with labels such as `A1`, `A2`, etc.
- **Destination Points**: Mark bot destinations with labels such as `B1`, `B2`, etc.
- **Obstacles**: Add obstacles to the grid by marking them as `X`, which bots will avoid.
- **Empty Spaces**: Mark open spaces in the grid with `.` where bots are free to move.

