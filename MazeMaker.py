import pickle  # For saving and loading

import pygame

import button

pygame.init()

# --- Constants ---
FPS = 60
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
LOWER_MARGIN = 50
SIDE_MARGIN = 200
ROWS = 50
COLS = 50
TILE_SIZE = SCREEN_HEIGHT // ROWS
SCROLL_SPEED = 1
FAST_SCROLL_SPEED = 5

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
DARK_GREY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- Game Variables ---
current_tool = "wall"  # Start with the wall drawing tool
start_point = None
end_point = None
scroll = 0
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_speed = SCROLL_SPEED
drawing = False  # Flag to track if the mouse button is held down for drawing
dragging_start = False  # Flag to track if dragging start point
dragging_end = False  # Flag to track if dragging end point

# --- Initialize Pygame ---
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Maze Designer')

# --- Load Images ---
# Button images
save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

# --- Font ---
font = pygame.font.SysFont('Futura', 24)


# --- Functions ---

def draw_text(text, font, text_col, x, y, centered=False):
    """Draws text on the screen."""
    img = font.render(text, True, text_col)
    if centered:
        x = x - img.get_width() // 2
    screen.blit(img, (x, y))


def draw_grid():
    """Draws the grid lines on the map."""
    # Vertical lines
    for c in range(COLS + 1):
        x = c * TILE_SIZE - scroll
        if 0 <= x <= SCREEN_WIDTH:  # Only draw if within screen bounds
            pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    # Horizontal lines
    for r in range(ROWS + 1):
        y = r * TILE_SIZE - scroll
        if 0 <= y <= SCREEN_HEIGHT:  # Only draw if within screen bounds
            pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))


def draw_maze():
    """Draws the maze elements (walls, start, end)."""
    for y, row in enumerate(maze_data):
        for x, tile in enumerate(row):
            rect = pygame.Rect((x * TILE_SIZE) - scroll, (y * TILE_SIZE) - scroll, TILE_SIZE, TILE_SIZE)

            if 0 <= rect.x <= SCREEN_WIDTH and 0 <= rect.y <= SCREEN_HEIGHT:
                if tile == 1:
                    pygame.draw.rect(screen, BLACK, rect)  # Wall
                elif tile == 2:
                    pygame.draw.rect(screen, GREEN, rect)  # Start
                elif tile == 3:
                    pygame.draw.rect(screen, RED, rect)  # End


def get_tile_coordinates(pos):
    """Calculates the tile coordinates (x, y) from a mouse position (pos)."""
    x = (pos[0] + scroll) // TILE_SIZE
    y = (pos[1] + scroll) // TILE_SIZE
    return x, y


def get_tile_rect(tile_pos):
    """Returns the pygame.Rect of a tile at the given tile coordinates."""
    x, y = tile_pos
    return pygame.Rect((x * TILE_SIZE) - scroll, (y * TILE_SIZE) - scroll, TILE_SIZE, TILE_SIZE)


def clear_points(point_type):
    """Clears all points of a specific type (2 for start, 3 for end) from the maze."""
    for r in range(ROWS):
        for c in range(COLS):
            if maze_data[r][c] == point_type:
                maze_data[r][c] = 0


def save_maze():
    """Saves the current maze data to a pickle file."""
    global maze_data
    try:
        with open('maze.pickle', 'wb') as file:
            pickle.dump(maze_data, file)
        print("Maze saved successfully!")
    except Exception as e:
        print(f"Error saving maze: {e}")


def load_maze():
    """Loads maze data from a pickle file."""
    global maze_data
    try:
        with open('maze.pickle', 'rb') as file:
            maze_data = pickle.load(file)
        print("Maze loaded successfully!")
    except FileNotFoundError:
        print("No saved maze found.")
    except Exception as e:
        print(f"Error loading maze: {e}")


# --- Maze Data (0: empty, 1: wall, 2: start, 3: end) ---
maze_data = [[0] * COLS for _ in range(ROWS)]

# --- Buttons ---
# Save and Load buttons
button_width = save_img.get_width()
button_spacing = 20
save_button = button.Button((SCREEN_WIDTH + SIDE_MARGIN) // 2 - button_width - button_spacing, SCREEN_HEIGHT + 10,
                            save_img, 1)
load_button = button.Button((SCREEN_WIDTH + SIDE_MARGIN) // 2 + button_spacing, SCREEN_HEIGHT + 10, load_img, 1)

# Tool selection buttons
wall_button = button.Button(SCREEN_WIDTH + 10, 10, font.render("Wall", True, WHITE), 1)
eraser_button = button.Button(SCREEN_WIDTH + 10, 10 + wall_button.rect.height + 10, font.render("Eraser", True, WHITE),
                              1)
start_button = button.Button(SCREEN_WIDTH + 10, 10 + 2 * (wall_button.rect.height + 10),
                             font.render("Start", True, WHITE), 1)
end_button = button.Button(SCREEN_WIDTH + 10, 10 + 3 * (wall_button.rect.height + 10), font.render("End", True, WHITE),
                           1)

# --- Main Game Loop ---
run = True
while run:
    clock.tick(FPS)

    # --- Draw ---
    screen.fill(GREY)  # Background
    draw_grid()
    draw_maze()

    # Draw UI Elements
    draw_text(f'Tool: {current_tool}', font, WHITE, 20, SCREEN_HEIGHT + 10)

    # Save and Load
    if save_button.draw(screen):
        save_maze()

    if load_button.draw(screen):
        load_maze()

    # --- Tool Panel ---
    pygame.draw.rect(screen, DARK_GREY, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # Tool Selection
    if wall_button.draw(screen):
        current_tool = "wall"
    if eraser_button.draw(screen):
        current_tool = "eraser"
    if start_button.draw(screen):
        current_tool = "start"
    if end_button.draw(screen):
        current_tool = "end"

    # Highlight selected tool
    if current_tool == "wall":
        pygame.draw.rect(screen, RED, wall_button.rect, 3)
    elif current_tool == "eraser":
        pygame.draw.rect(screen, RED, eraser_button.rect, 3)
    elif current_tool == "start":
        pygame.draw.rect(screen, RED, start_button.rect, 3)
    elif current_tool == "end":
        pygame.draw.rect(screen, RED, end_button.rect, 3)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = FAST_SCROLL_SPEED

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = SCROLL_SPEED

        # --- Mouse Handling ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x, y = get_tile_coordinates(event.pos)  # Error corrected

            if 0 <= x < COLS and 0 <= y < ROWS:
                if current_tool == "wall":
                    maze_data[y][x] = 1
                elif current_tool == "eraser":
                    maze_data[y][x] = 0
                elif current_tool == "start":
                    clear_points(2)
                    maze_data[y][x] = 2
                    start_point = (x, y)
                elif current_tool == "end":
                    clear_points(3)
                    maze_data[y][x] = 3
                    end_point = (x, y)
            # Check if start or end point is being dragged
            if current_tool == "start" and start_point and get_tile_rect(start_point).collidepoint(event.pos):
                dragging_start = True
            if current_tool == "end" and end_point and get_tile_rect(end_point).collidepoint(event.pos):
                dragging_end = True

        if event.type == pygame.MOUSEMOTION:
            x, y = get_tile_coordinates(event.pos)
            if drawing:
                if 0 <= x < COLS and 0 <= y < ROWS:
                    if current_tool == "wall":
                        maze_data[y][x] = 1
                    elif current_tool == "eraser":
                        maze_data[y][x] = 0
            # Drag start/end points
            if dragging_start and 0 <= x < COLS and 0 <= y < ROWS:
                clear_points(2)
                maze_data[y][x] = 2
                start_point = (x, y)
            if dragging_end and 0 <= x < COLS and 0 <= y < ROWS:
                clear_points(3)
                maze_data[y][x] = 3
                end_point = (x, y)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            dragging_start = False
            dragging_end = False

    # --- Scrolling ---
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed
    if scroll_up and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_down and scroll < (ROWS * TILE_SIZE) - SCREEN_HEIGHT:
        scroll += 5 * scroll_speed

    # --- Update Display ---
    pygame.display.update()

pygame.quit()
