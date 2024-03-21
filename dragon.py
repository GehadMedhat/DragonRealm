import random
import pygame
import sys

# Initialize pygame
pygame.init()

# Create the screen
screen_width, screen_height = 1000, 495
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
background = pygame.image.load('background.png')

# Caption and Icon
pygame.display.set_caption("Dragon Realm")
icon = pygame.image.load('dragon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (100, 100))  # Set the size of the player

# Set the initial player position to the middle of the screen
playerX = 450
playerY = 500
playerX_change = 0
playerY_change = 0

# Cave images
cave_left = pygame.image.load('cave.png')
cave_right = pygame.image.load('cave.png')
cave_left = pygame.transform.scale(cave_left, (200, 200))
cave_right = pygame.transform.scale(cave_right, (200, 200))

# Set cave positions
cave_left_x = 50
cave_left_y = 100

cave_right_x = 750
cave_right_y = 100

# Font for button text
font = pygame.font.Font(None, 36)

# Function to check if a point is inside a rectangle
def is_point_inside_rect(point, rect):
    return rect.left <= point[0] <= rect.right and rect.top <= point[1] <= rect.bottom

def player(x, y):
    screen.blit(playerImg, (x, y))

def show_caves():
    screen.blit(cave_left, (cave_left_x, cave_left_y))
    screen.blit(cave_right, (cave_right_x, cave_right_y))

def show_result(result_text):
    result_surface = font.render(result_text, True, (255, 255, 255))
    result_rect = result_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    result_screen = pygame.Surface((screen_width, screen_height))  # Create a new surface for the result
    result_screen.fill((0, 0, 0))
    result_screen.blit(result_surface, result_rect)

    screen.blit(result_screen, (0, 0))

    pygame.display.flip()

# Randomly choose which cave is deadly
deadly_cave = random.choice(["left", "right"])

# Game states
MOVING_STATE = 0
CHOOSING_CAVE_STATE = 1
RESULT_STATE = 2
PLAY_AGAIN_STATE = 3

# Initial game state
current_state = MOVING_STATE

# Game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses while in RESULT_STATE or PLAY_AGAIN_STATE
        if event.type == pygame.KEYDOWN:
            if current_state == RESULT_STATE:
                if event.key == pygame.K_y:
                    current_state = PLAY_AGAIN_STATE
                    deadly_cave = random.choice(["left", "right"])  # Randomly choose deadly cave again
                elif event.key == pygame.K_n:
                    running = False
            elif current_state == PLAY_AGAIN_STATE:
                if event.key == pygame.K_y:
                    current_state = MOVING_STATE
                elif event.key == pygame.K_n:
                    running = False

    # Update player position
    playerX += playerX_change
    playerY += playerY_change

    # Set the boundaries
    if playerX < 0:
        playerX = 0
    elif playerX > screen_width - 100:
        playerX = screen_width - 100

    if playerY < 0:
        playerY = 0
    elif playerY > screen_height - 100:
        playerY = screen_height - 100

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    show_caves()
    player(playerX, playerY)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if current_state == MOVING_STATE:
        # Check if the mouse is over the photo and the left button is pressed
        if is_point_inside_rect((mouse_x, mouse_y), pygame.Rect(cave_left_x, cave_left_y, 200, 200)) and pygame.mouse.get_pressed()[0]:
            chosen_cave = "left"
            current_state = RESULT_STATE
        elif is_point_inside_rect((mouse_x, mouse_y), pygame.Rect(cave_right_x, cave_right_y, 200, 200)) and pygame.mouse.get_pressed()[0]:
            chosen_cave = "right"
            current_state = RESULT_STATE

    elif current_state == RESULT_STATE:
        result_text = "You died!" if chosen_cave == deadly_cave else "You survived!"
        result_text += " Press 'Y' to play again or 'N' to quit."
        show_result(result_text)
        pygame.display.flip()  # Update the display
        pygame.time.delay(3000)  # Display the result for 3 seconds

    elif current_state == PLAY_AGAIN_STATE:
        show_result("Do you want to play again? (Y/N)")
        pygame.display.flip()  # Update the display

    pygame.display.flip()

pygame.quit()
sys.exit()
