import pygame
import pygame_gui
import sys
import os
import importlib
from draw_context import DrawContext

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
debug_font = pygame.font.SysFont(None, 30)

# Load designs
designs = []
design_dir = 'designs'
for filename in os.listdir(design_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = importlib.import_module(f'{design_dir}.{module_name}')
        design_name, design_instance = module.register_design()
        designs.append((design_name, design_instance))

# Sort designs by name
designs.sort(key=lambda x: x[0])

# Menu options
menu_options = [design[0] for design in designs]
selected_option = 0

def draw_menu():
    screen.fill((0, 0, 0))
    for i, option in enumerate(menu_options):
        color = (255, 255, 255) if i == selected_option else (100, 100, 100)
        text = menu_font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))
        screen.blit(text, text_rect)
    pygame.display.flip()

# Initialize the clock
clock = pygame.time.Clock()

# Initialize pygame_gui
manager = pygame_gui.UIManager((screen_width, screen_height))

# Main loop
running = True
current_frame = 0
total_frames = 1000  # Example total frames
in_menu = True
selected_option = 0
menu_options = [design[0] for design in designs]
paused = False
show_debug = True

while running:
    time_delta = clock.tick(60) / 1000.0  # Time in seconds since last frame

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
                    # Initialize the selected design
                    designs[selected_option][1].init(manager)
            else:
                if event.key == pygame.K_ESCAPE:
                    in_menu = True
                    # Uninitialize the selected design
                    designs[selected_option][1].uninit()
                elif event.key == pygame.K_LEFT:
                    current_frame = max(0, current_frame - 1)
                elif event.key == pygame.K_RIGHT:
                    current_frame = min(total_frames - 1, current_frame + 1)
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_d:
                    show_debug = not show_debug

        if not in_menu:
            manager.process_events(event)
            designs[selected_option][1].process_event(event, manager)

    keys = pygame.key.get_pressed()
    if not in_menu and not paused:
        if keys[pygame.K_LEFT]:
            current_frame = max(0, current_frame - 1)
        elif keys[pygame.K_RIGHT]:
            current_frame = min(total_frames - 1, current_frame + 1)
    
    if not in_menu:
        manager.update(time_delta)

    context = DrawContext(screen, font, current_frame, total_frames, screen_width, screen_height)
    
    if in_menu:
        draw_menu()
    else:
        designs[selected_option][1].draw_design(context)
    
    if not paused:
        current_frame += 1

    # Calculate FPS
    fps = clock.get_fps()

    # Render FPS if debug information is enabled
    if show_debug:
        fps_text = debug_font.render(f"FPS: {fps:.2f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        
    if not in_menu:
        # Render the UI
        manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()