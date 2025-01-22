import pygame
import sys
from svgtopng import *
from hard import *
from easy import *
from medium import *

pygame.init()

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (106, 158, 208)
DARK_BLUE = (0, 0, 139)
GRAY = (192, 192, 192)

# Fonts

button_font = pygame.font.SysFont("poppins", 60)

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
BUTTON_PADDING = 20

buttons = {
    "Easy": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.8 - BUTTON_HEIGHT - BUTTON_PADDING},
    "Medium": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.8},
    "Hard": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.8 + BUTTON_HEIGHT + BUTTON_PADDING},
}




def draw_homepage(mouse_pos=None):
    screen.fill(LIGHT_BLUE)


    svg_rect = svg_image.get_rect(center=(width // 2, height // 4))     #  1/4th of the way down from the top.
    screen.blit(svg_image, svg_rect)

    # Draw buttons
    for label, button in buttons.items():
        rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = mouse_pos and rect.collidepoint(mouse_pos)

        # Button color and shadow
        color = GRAY if is_hovered else BLUE
        shadow_color = BLACK
        pygame.draw.rect(screen, shadow_color, rect.move(5, 5), border_radius=10)  # Shadow
        pygame.draw.rect(screen, color, rect, border_radius=10)  # Main button

        # Button text
        text_surface = button_font.render(label, True, WHITE)
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery))
        screen.blit(text_surface, text_rect)

    pygame.display.update()


# Initialize screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

# Draw the homepage
draw_homepage()

game_over = False

while not game_over:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            button_rect_h = pygame.Rect(buttons["Hard"]["x"], buttons["Hard"]["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
            button_rect_m = pygame.Rect(buttons["Medium"]["x"], buttons["Medium"]["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
            button_rect_e = pygame.Rect(buttons["Easy"]["x"], buttons["Easy"]["y"], BUTTON_WIDTH, BUTTON_HEIGHT)

            if button_rect_h.collidepoint(pos):
                gameplay_hard()
            if button_rect_m.collidepoint(pos):
                gameplay_medium()
            if button_rect_e.collidepoint(pos):
                gameplay_easy()

    draw_homepage(mouse_pos)
