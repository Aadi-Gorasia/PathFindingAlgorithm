# PathFindingAlgorithm

**1. Imports:**

*   `pygame`: A popular library for creating games and multimedia applications in Python. It's used here for graphics, event handling, and the main game loop.
*   `math`: The standard Python math library, likely used for distance calculations (though not explicitly used in the `h` function, it could be used for Euclidean distance).
*   `queue.PriorityQueue`: Used to implement the A\* algorithm's open set. A priority queue automatically sorts elements based on their priority (in this case, the f-score of nodes).
*   `pickle`: Used to load maze data that has been saved (serialized) into a file (`maze.pickle`).

**2. Constants:**

*   `WIDTH`: Sets the width (and height) of the game window.
*   `WIN`: Creates the main game display window using `pygame.display.set_mode()`.
*   `pygame.display.set_caption()`: Sets the title of the window.
*   Color constants (e.g., `RED`, `GREEN`, `BLACK`, etc.): Define RGB color values for different visual elements in the program.

**3. Spot Class:**

*   Represents a single node (or "spot") in the grid.
*   **`__init__`:** Initializes a Spot object with:
    *   `row`, `col`: Its row and column indices in the grid.
    *   `x`, `y`: Its pixel coordinates on the screen.
    *   `color`: Its initial color (default is `WHITE`).
    *   `neighbors`: An empty list to store its neighboring Spots (will be populated later).
    *   `width`: The width of the Spot in pixels.
    *   `total_rows`: The total number of rows in the grid.
*   **`get_pos()`:** Returns the Spot's row and column.
*   **`is_closed()`, `is_open()`, `is_barrier()`, `is_start()`, `is_end()`:** These are boolean methods that check the Spot's color to determine its state (e.g., closed, open, barrier, start, or end).
*   **`reset()`, `make_start()`, `make_closed()`, `make_open()`, `make_barrier()`, `make_end()`, `make_path()`:** Methods that set the Spot's color to represent its state visually.
*   **`draw()`:** Draws the Spot as a rectangle on the screen (`win`).
*   **`update_neighbors()`:** Calculates the valid neighboring Spots of the current Spot and adds them to its `neighbors` list. It considers the grid boundaries and barrier spots to only include valid, non-barrier neighbors. Allows for diagonal movements.
*   **`__lt__`:** Defines how Spots are compared. The less than (`<`) operator will determine the order in the PriorityQueue. This function here just return `False`, but the order will depend in the `f\_score` inside `algorithm()`.

**4. `h(p1, p2)` (Heuristic Function):**

*   Calculates the Manhattan distance between two points, allows diagonal distance to cost less then if going orthogonal first and then diagonal.
    *   `p1`, `p2`: The two points (tuples of (x, y) coordinates).
*   Manhattan distance is an appropriate heuristic for pathfinding where movement is restricted to horizontal and vertical (and diagonal) steps, as it never overestimates the actual cost to reach the goal.

**5. `reconstruct_path(came_from, current, draw)`:**

*   Backtracks from the end node to the start node to construct the shortest path found by the A\* algorithm.
    *   `came_from`: A dictionary that maps a Spot to the Spot from which it was reached.
    *   `current`: The current Spot (initially the end node).
    *   `draw`: The drawing function, used to update the display after each Spot is marked as part of the path.
*   The `while` loop iterates as long as the current Spot is in the `came_from` dictionary, effectively following the path back to the start node.
*   Inside the loop:
    *   It updates the current spot's color to indicate it's on the path (using `make_path()`).
    *   It updates the display by calling the `draw()` function.

**6. `algorithm(draw, grid, start, end)` (A\* Pathfinding Algorithm):**

*   Implements the core A\* search algorithm.
*   **Initialization:**
    *   `count`: Used to break ties in the PriorityQueue when two Spots have the same f-score.
    *   `open_set`: A PriorityQueue to store the Spots that need to be evaluated, ordered by their f-score.
    *   `came_from`: A dictionary to store the path (which Spot came from which).
    *   `g_score`: A dictionary storing the cost of the shortest path found so far from the start to each Spot.
    *   `f_score`: A dictionary storing the estimated total cost (g-score + heuristic) from the start to the end through each Spot.
    *   `open_set_hash`: A set for efficiently checking if a Spot is in the `open_set`.
*   **Main Loop (while not open\_set.empty()):**
    *   Handles Pygame events to check for the user quitting the application.
    *   Retrieves the Spot with the lowest f-score from the `open_set`.
    *   If the `current` Spot is the `end`, it calls `reconstruct_path()` to draw the path and returns `True` (path found).
    *   **Neighbor Exploration (for neighbor in current.neighbors):**
        *   Calculates the tentative `temp_g_score` to reach the `neighbor`. Allows for diagonal movements
        *   If `temp_g_score` is less than the current `g_score` for the neighbor (meaning a shorter path has been found), it:
            *   Updates `came_from` to indicate that we reached the `neighbor` from `current`.
            *   Updates `g_score` and `f_score` for the `neighbor`.
            *   If the `neighbor` is not already in the `open_set`, add it to the `open_set` and `open_set_hash`.
            *   Set the color of the neighbor to indicate it has been opened (using `make_open()`).
    *   Calls the `draw()` function to update the display.
    *   If the `current` Spot is not the `start` node, set its color to indicate that it has been closed.
*   Returns `False` if the open set is empty and the end node has not been reached (no path found).

**7. `make_grid(rows, width)`:**

*   Creates a new grid of Spots.
*   Calculates the `gap` (width of each Spot) based on the total `width` and number of `rows`.
*   Uses nested loops to iterate through rows and columns:
    *   Creates a `Spot` object for each cell and adds it to the `grid`.
*   Returns the created `grid`.

**8. `load_grid_from_pickle(pickle_file, rows, width)`:**

*   Loads a grid from a pickle file (`maze.pickle` by default).
*   **File Loading:**
    *   Opens the specified `pickle_file` in binary read mode (`'rb'`).
    *   Uses `pickle.load(file)` to load the serialized data from the file into `grid_data`.
*   **Error Handling:**
    *   Uses `try...except` blocks to handle potential errors:
        *   `FileNotFoundError`: If the pickle file doesn't exist.
        *   `pickle.PickleError`: If there is an issue with the pickle file format or data.
        *   `ValueError`: Handles issues with data format within the pickle file.
        *   `Exception`: Catches any other unexpected errors.
*   **Grid Creation and Population:**
    *   Creates a new, empty grid of Spots using `make_grid()`.
    *   Iterates through the loaded `grid_data`, and for each cell where `is_barrier` is `True`, sets the corresponding `Spot` in the grid as a barrier using `make_barrier()`. Note the transposing fix using `j` (columns) then `i` (rows)
*   Returns the loaded `grid`.

**9. `draw_grid(win, rows, width)`:**

*   Draws the grid lines on the screen.
*   Calculates the `gap` (width of each cell).
*   Uses loops to draw horizontal and vertical lines, creating the grid.

**10. `draw(win, grid, rows, width)`:**

*   The main drawing function.
*   Fills the screen with `WHITE`.
*   Iterates through all Spots in the `grid` and calls each Spot's `draw()` method to draw it on the screen.
*   Draws the grid lines by calling `draw_grid()`.
*   Updates the display using `pygame.display.update()` to show the changes.

**11. `get_clicked_pos(pos, rows, width)`:**

*   Converts mouse click coordinates to grid row and column indices.
    *   `pos`: The mouse click position (x, y).
*   Calculates the `gap` (width of each cell).
*   Divides the x and y coordinates of the click by the `gap` to determine the row and column.
*   Returns the `row` and `col`.

**12. `main(win, width)`:**

*   The main game loop function.
*   **Initialization:**
    *   `ROWS`: Sets the number of rows in the grid.
    *   `grid`: Loads the grid from the pickle file.
    *   `start`, `end`: Initialized to `None` (no start or end Spot selected initially).
*   **Main Loop (while run):**
    *   Calls `draw()` to draw the grid.
    *   Handles Pygame events:
        *   **`pygame.QUIT`:** Quits the application if the user closes the window.
        *   **`pygame.mouse.get_pressed()[0]` (Left Mouse Button):**
            *   Gets the clicked position.
            *   Converts the position to a `row` and `col` using `get_clicked_pos()`.
            *   Gets the clicked `Spot`.
            *   If `start` is not set and the Spot is not a barrier or `end`, makes the clicked Spot the `start`.
            *   If `end` is not set and the Spot is not a barrier or `start`, makes the clicked Spot the `end`.
        *   **`pygame.mouse.get_pressed()[2]` (Right Mouse Button):**
            *   Gets the clicked position.
            *   Converts the position to a `row` and `col`.
            *   Resets the clicked `Spot`.
            *   If the clicked Spot was the `start`, set `start` to `None`.
            *   If the clicked Spot was the `end`, set `end` to `None`.
        *   **`pygame.KEYDOWN`:**
            *   **`pygame.K_SPACE`:** If both `start` and `end` are set, it starts the A\* algorithm:
                *   Updates the neighbors of each Spot using `update_neighbors()`.
                *   Calls the `algorithm()` function to find the path.
            *   **`pygame.K_c`:** Clears the grid, resets `start` and `end`, and reloads the grid from the pickle file (resets the maze to its initial state).
*   Exits using `pygame.quit()`.

**In Summary:**

This code implements a visual demonstration of the A\* pathfinding algorithm. It allows the user to select a start and end point in a grid-based maze (loaded from a pickle file) and then runs the A\* algorithm to find the shortest path between them. The program visualizes the steps of the algorithm, showing which nodes are opened and closed during the search, and finally draws the shortest path found.
