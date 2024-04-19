import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 440  # Increased height to accommodate the drop-down menu
COLOR_BOX_SIZE = 40
NUM_ROWS = 6
NUM_COLS = 6

# Colors
colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 255) # White
]

# Function to draw color boxes
def draw_color_boxes(screen):
    for i, color in enumerate(colors):
        row = i // NUM_COLS
        col = i % NUM_COLS
        pygame.draw.rect(screen, color, (col * COLOR_BOX_SIZE, row * COLOR_BOX_SIZE + 40, COLOR_BOX_SIZE, COLOR_BOX_SIZE))

# Function to get selected color
def get_selected_color(mouse_pos):
    col = mouse_pos[0] // COLOR_BOX_SIZE
    row = (mouse_pos[1] - 40) // COLOR_BOX_SIZE
    index = row * NUM_COLS + col
    if index < len(colors):
        return colors[index]
    else:
        return None

# Function to handle drop-down menu
def handle_dropdown_menu(mouse_pos):
    col = mouse_pos[0] // 100
    if 0 <= col < 3:
        return col + 1
    else:
        return None

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Color Selector")

    # Define fonts
    font = pygame.font.Font(None, 36)

    # Define menu items
    menu_items = ["1", "2", "3"]

    selected_option = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if 0 <= event.pos[1] < 40:  # Check if mouse click is in the menu area
                        selected_option = handle_dropdown_menu(event.pos)
                    else:
                        selected_color = get_selected_color(event.pos)
                        if selected_color is not None:
                            print("Selected Color:", selected_color)
                            # Here you can perform actions with the selected color

        screen.fill((255, 255, 255))

        # Draw menu
        for i, item in enumerate(menu_items):
            text = font.render(item, True, (0, 0, 0))
            screen.blit(text, (10 + i * 100, 10))

        draw_color_boxes(screen)

        # Draw selected option highlight
        if selected_option is not None:
            pygame.draw.rect(screen, (200, 200, 200), (selected_option * 100 - 95, 5, 90, 30), 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
