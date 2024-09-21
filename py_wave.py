import pygame
import sys
import os
import importlib

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1280, 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Py-Wave')

# Define the text and font
font_size = 100
font = pygame.font.SysFont(None, font_size)
menu_font = pygame.font.SysFont(None, 50)

# Load designs
designs = []
design_dir = 'designs'
for filename in os.listdir(design_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = importlib.import_module(f'{design_dir}.{module_name}')
        design_name, design_func = module.register_design()
        designs.append((design_name, design_func))

# Sort designs by name
designs.sort(key=lambda x: x[0])

# Menu options
menu_options = [design[0] for design in designs]
selected_option = 0

# Frame tracking
current_frame = 0
total_frames = 100  # Example total number of frames

def draw_menu():
    screen.fill((0, 0, 0))
    for i, option in enumerate(menu_options):
        color = (255, 255, 255) if i == selected_option else (100, 100, 100)
        text = menu_font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))
        screen.blit(text, text_rect)
    pygame.display.flip()

# Main loop
in_menu = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if in_menu:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    in_menu = False
            else:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True
                elif event.key == pygame.K_LEFT:
                    current_frame = max(0, current_frame - 1)
                elif event.key == pygame.K_RIGHT:
                    current_frame = min(total_frames - 1, current_frame + 1)

    if in_menu:
        draw_menu()
    else:
        designs[selected_option][1](screen, font, current_frame)

# Quit Pygame
pygame.quit()
sys.exit()