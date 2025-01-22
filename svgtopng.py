import pygame
import cairosvg  # To handle SVGs
from io import BytesIO 



def load_svg_as_surface(file_path, width, height):
    with open(file_path, 'rb') as svg_file:
        svg_data = svg_file.read()

    # Convert SVG to PNG bytes
    png_bytes = BytesIO(cairosvg.svg2png(bytestring=svg_data, output_width=width, output_height=height))

    # Load PNG bytes into a Pygame image
    png_surface = pygame.image.load(png_bytes, "png")
    return png_surface

svg_image = load_svg_as_surface("connect-four.svg", 700, 700)