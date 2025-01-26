# A\* Pathfinding Algorithm Visualization

This project demonstrates the A\* search algorithm visually using Pygame. It loads a maze from a `.pickle` file, allowing you to select a start and end point and then visualize the algorithm finding the shortest path.

## How to Use

1. **Install Dependencies:**
    ```bash
    pip install pygame
    ```

2. **Prepare the Maze:**
    *   A `maze.pickle` file is expected, containing a 2D list representation of the maze (where `True` indicates a barrier). You'll need to create this file using a separate script to define your maze layout and save it using the `pickle` library in python. Ensure the format is `[[False, False, True, ...], [True, False, ...]]`

3. **Run the Visualization:**
    ```bash
    python your_script_name.py 
    ```
    Replace `your_script_name.py` with the name of the Python file containing the code.

4. **Interacting with the Maze:**
    *   **Left-click:** Set the start point (orange) or the end point (turquoise) on empty cells.
    *   **Right-click:** Reset a cell (remove start, end, or barrier if placed).
    *   **Spacebar:** Start the A\* pathfinding algorithm.
    *   **C Key:** Clear the path and reload the maze from the `maze.pickle` file.

**Enjoy visualizing the A\* algorithm in action!**
