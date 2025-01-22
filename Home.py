import pygame
import sys
import random
from svgtopng import svg_image
from hard import gameplay_hard
from easy import gameplay_easy
from medium import gameplay_medium

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

# New lighter button colors
LIGHTER_BLUE = (135, 206, 250)
HOVER_BLUE = (173, 216, 230)

# Fonts
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 40)  # Default bold font for buttons

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
BUTTON_PADDING = 20

buttons = {
    "Easy": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.5 - BUTTON_HEIGHT - BUTTON_PADDING},
    "Medium": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.5},
    "Hard": {"x": width // 2 - BUTTON_WIDTH // 2, "y": height // 1.5 + BUTTON_HEIGHT + BUTTON_PADDING},
}

# Initialize screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")

# Load background image
background = pygame.image.load("picture.png")
background = pygame.transform.scale(background, size)

def create_gradient(color1, color2, height):
    gradient = pygame.Surface((1, height))
    for i in range(height):
        r = color1[0] * (height - i) / height + color2[0] * i / height
        g = color1[1] * (height - i) / height + color2[1] * i / height
        b = color1[2] * (height - i) / height + color2[2] * i / height
        gradient.set_at((0, i), (int(r), int(g), int(b)))
    return gradient

gradient = create_gradient(LIGHT_BLUE, DARK_BLUE, height)
gradient = pygame.transform.scale(gradient, (width, height))

def draw_button(surface, label, x, y, width, height, text_color, button_color, hover=False):
    # Button shadow
    shadow_color = (0, 0, 0, 100)
    shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, shadow_color, (0, 0, width, height), border_radius=15)
    surface.blit(shadow_surface, (x + 3, y + 3))

    # Button body
    pygame.draw.rect(surface, button_color, (x, y, width, height), border_radius=15)
    
    # Button outline
    outline_color = WHITE if hover else button_color
    pygame.draw.rect(surface, outline_color, (x, y, width, height), 2, border_radius=15)
    
    # Button text
    text = button_font.render(label, True, text_color)
    text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text, text_rect)

    # Button shine effect
    if hover:
        shine_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(shine_surface, (255, 255, 255, 30), (0, 0, width, height // 2), border_radius=15)
        surface.blit(shine_surface, (x, y))

def draw_homepage(mouse_pos=None):
    screen.blit(background, (0, 0))

    # Draw buttons with hover effect
    for label, button in buttons.items():
        rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
        is_hovered = mouse_pos and rect.collidepoint(mouse_pos)
        
        # Use new lighter blue colors
        button_color = LIGHTER_BLUE if not is_hovered else HOVER_BLUE
        text_color = WHITE
        
        draw_button(screen, label, button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT, text_color, button_color, is_hovered)

    pygame.display.update()

# Animation variables
particles = []

def create_particle(x, y):
    return {
        "x": x,
        "y": y,
        "radius": random.randint(2, 5),
        "dx": random.uniform(-1, 1),
        "dy": random.uniform(-1, 1),
        "color": random.choice([RED, YELLOW, BLUE, WHITE]),
        "life": random.randint(30, 60)
    }

def update_particles():
    for particle in particles[:]:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["life"] -= 1
        if particle["life"] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), particle["radius"])

game_over = False
clock = pygame.time.Clock()

while not game_over:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for label, button in buttons.items():
                rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
                if rect.collidepoint(pos):
                    if label == "Hard":
                        gameplay_hard()
                    elif label == "Medium":
                        gameplay_medium()
                    elif label == "Easy":
                        gameplay_easy()

    # Create particles
    if random.random() < 0.1:
        particles.append(create_particle(random.randint(0, width), random.randint(0, height)))

    update_particles()
    draw_homepage(mouse_pos)
    draw_particles()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
 