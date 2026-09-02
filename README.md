# Pathfinding Visualiser
An interactive Python application for visualising and comparing the BFS, Dijkstra's, and A* pathfinding algorithms.

## Features:
- Resizable grid (up to 300x300)
- Drawing modes
- Can select between BFS, Dijkstra's and A* algorithms
- Weighted cells for Dijkstra's algorithm
- Slowed down animation for visualisation
- A clear all button
- A grid showing a table of results for comparison of the different algorithms (can compare the total number of nodes visited, the total number of cells in the path, the time taken to complete and the cost of the cells)

## How to run:
1. Install python
2. Install CustomTkinter (pip install customtkinter)

## Algorithms:
- BFS (Breadth-First Search): Explores the grid level by level, expanding outwards from the start node. Uses a queue to ensure that nodes are visited in the order they are discovered. It does not account for the weight of each cell, so may pick a more expensive route.
- Dijkstra's: Similar to BFS, but accounts for weighted cells. Finds the lowest cost route rather than the shortest, so will go through weighted cells only if it means the route will be cheaper overall. Uses a priority queue so that the node with the lowest total cost is explored next. Normal cells have a cost of 1 whereas weighted ones have a cost of 5.
- A*: Builds on Dijkstra's by also estimating how far each node is from the destination, giving it a sense of direction. Considers f(n) = g(n) + h(n) for each node where g(n) is the known cost from the start node to the current node, h(n) is the estimated remaining distance to the end node and f(n) is the estimated total cost of a path through that node. Uses Manhattan distance as the heuristic because movement is restricted to only 4 directions. Guides the search towards the destination, allowing A* to explore fewer nodes than Dijkstra's.

## How to use:
- If you would like to change the grid size, type the new grid size in the dimensions and press apply
- Start off by drawing the maze you want
- Add weighted cells if needed
- If you make a mistake, use the erase tool in the drawing mode to correct it
- Place your start and end nodes
- Select the algorithm you would like to solve your maze
- Select whether you would like the search to be animated or not by selecting the checkbox
- When ready, press Run
    - If you selected for the path to be animated, you should see the cells turn blue while exploring. These are the nodes that are being considered by the algorithm, and when it reaches the end node, you should see the final path appear in yellow
    - If you selected for the path to not be animated, the final path should show up right away
- If you would like to compare other algorithms against your maze, change only the algorithm, and the new results will appear in the table alongside the algorithm used
    - Changing anything else will erase the results from the table
- When you would like to delete everyting and start over, press the Clear button
    - This will delete everything from the grid, as well as the results in the table

## Results explained:
The Results table shows 4 different numbers - Nodes visited, Path, Time taken and Cost
- Nodes visited: The total number of moves the algorithm considered while searching for the end node
    - This is the total number of yellow squares plus the end node
- Path: The total length of moves in the final path from start node to end node
    - This is the total number of yellow squares plus the end one
- Time taken: The total amount of time the algorithm took to find the optimal path
- Cost: The total cost of the path (where white squares have a cost of 1 and orange ones have a cost of 5)
- You may also see beneath the results table, there is the estimated animation duration and how much slower the animation is relative to the actual amount of time the algorithm took to execute
    - The animation timing cannot be predicted perfectly because each frame is scheduled through the Tkinter event loop. The program therefore first displays an estimate then shows the actual animation duration once it has finished