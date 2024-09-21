from base_design import BaseDesign
from color_palettes import ColorPalettes
import pygame
import pygame_gui
import math

class SineWaveDesign(BaseDesign):
    def __init__(self):
        self.amplitude_slider = None
        self.frequency_slider = None
        self.num_waves_slider = None
        self.modulation_frequency_slider = None
        self.line_width_slider = None
        self.rotation_slider = None
        self.amplitude_label = None
        self.frequency_label = None
        self.num_waves_label = None
        self.modulation_frequency_label = None
        self.line_width_label = None
        self.rotation_label = None
        self.amplitude_button = None
        self.frequency_button = None
        self.num_waves_button = None
        self.amplitude_dial = None
        self.frequency_dial = None
        self.num_waves_dial = None
        self.amplitude_value_label = None
        self.frequency_value_label = None
        self.num_waves_value_label = None
        self.modulation_frequency_value_label = None
        self.line_width_value_label = None
        self.rotation_value_label = None
        self.modulation_enabled = {
            'amplitude': False,
            'frequency': False,
            'num_waves': False
        }
        self.start_time = pygame.time.get_ticks()

    def init(self, manager):
        # Create sliders
        self.amplitude_slider = self.create_slider((50, 50), 100, (10, 200), manager)
        self.frequency_slider = self.create_slider((50, 100), 0.01, (0.001, 0.1), manager)
        self.num_waves_slider = self.create_slider((50, 150), 20, (1, 50), manager)
        self.modulation_frequency_slider = self.create_slider((50, 200), 1, (0.001, 0.2), manager)
        self.line_width_slider = self.create_slider((50, 250), 1, (1, 10), manager)
        self.rotation_slider = self.create_slider((50, 300), 0, (0, 360), manager)

        # Create labels
        self.amplitude_label = self.create_label((260, 50), 'Amplitude', manager)
        self.frequency_label = self.create_label((260, 100), 'Frequency', manager)
        self.num_waves_label = self.create_label((260, 150), 'Num Waves', manager)
        self.modulation_frequency_label = self.create_label((260, 200), 'Modulation Freq', manager)
        self.line_width_label = self.create_label((260, 250), 'Line Width', manager)
        self.rotation_label = self.create_label((260, 300), 'Rotation', manager)

        # Create buttons
        self.amplitude_button = self.create_button((370, 50), 'Modulate', manager)
        self.frequency_button = self.create_button((370, 100), 'Modulate', manager)
        self.num_waves_button = self.create_button((370, 150), 'Modulate', manager)

        # Create value labels
        self.amplitude_value_label = self.create_label((480, 50), '', manager)
        self.frequency_value_label = self.create_label((480, 100), '', manager)
        self.num_waves_value_label = self.create_label((480, 150), '', manager)
        self.modulation_frequency_value_label = self.create_label((480, 200), '', manager)
        self.line_width_value_label = self.create_label((480, 250), '', manager)
        self.rotation_value_label = self.create_label((480, 300), '', manager)

    def create_slider(self, position, start_value, value_range, manager):
        return pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(position, (200, 30)),
            start_value=start_value,
            value_range=value_range,
            manager=manager
        )

    def create_label(self, position, text, manager):
        return pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position, (100, 30)),
            text=text,
            manager=manager
        )

    def create_button(self, position, text, manager):
        return pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (100, 30)),
            text=text,
            manager=manager
        )

    def toggle_modulation(self, dial, position, start_value, value_range, manager, key):
        if dial is None:
            dial = self.create_slider(position, start_value, value_range, manager)
            self.modulation_enabled[key] = True
        else:
            dial.kill()
            dial = None
            self.modulation_enabled[key] = False
        return dial

    def update_value_range(self, dial, slider, min_value):
        if dial:
            new_range = dial.get_current_value()
            slider.value_range = (min_value, new_range)

    def uninit(self):
        # Remove sliders, labels, buttons, and dials
        elements = [
            self.amplitude_slider, self.frequency_slider, self.num_waves_slider, self.modulation_frequency_slider,
            self.line_width_slider, self.rotation_slider,
            self.amplitude_label, self.frequency_label, self.num_waves_label, self.modulation_frequency_label,
            self.line_width_label, self.rotation_label,
            self.amplitude_button, self.frequency_button, self.num_waves_button,
            self.amplitude_dial, self.frequency_dial, self.num_waves_dial,
            self.amplitude_value_label, self.frequency_value_label, self.num_waves_value_label, self.modulation_frequency_value_label,
            self.line_width_value_label, self.rotation_value_label
        ]
        for element in elements:
            if element:
                element.kill()
        self.__init__()

    def draw_design(self, context):
        # Sine wave parameters
        base_amplitude = self.amplitude_slider.get_current_value() if self.amplitude_slider else 100
        frequency = self.frequency_slider.get_current_value() if self.frequency_slider else 0.01
        num_waves = int(self.num_waves_slider.get_current_value()) if self.num_waves_slider else 20
        modulation_frequency = self.modulation_frequency_slider.get_current_value() if self.modulation_frequency_slider else 1
        line_width = int(self.line_width_slider.get_current_value()) if self.line_width_slider else 1
        rotation = self.rotation_slider.get_current_value() if self.rotation_slider else 0
        phase_shift = context.frame * 0.05  # Phase shift changes with the current frame
        amplitude_decrement = base_amplitude / num_waves  # Amplitude decrement for each wave

        # Modulate values if enabled
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - self.start_time) / 1000.0  # Time in seconds

        if self.modulation_enabled['amplitude']:
            base_amplitude = 100 + 50 * math.sin(2 * math.pi * modulation_frequency * time_elapsed)
            base_amplitude *= self.amplitude_dial.get_current_value()
        if self.modulation_enabled['frequency']:
            frequency = 0.01 + 0.005 * math.sin(2 * math.pi * modulation_frequency * time_elapsed)
            frequency *= self.frequency_dial.get_current_value()
        if self.modulation_enabled['num_waves']:
            num_waves = int(20 + 5 * math.sin(2 * math.pi * modulation_frequency * time_elapsed))
            num_waves *= self.num_waves_dial.get_current_value()
        
        # Update value labels
        self.amplitude_value_label.set_text(f'{base_amplitude:.2f}')
        self.frequency_value_label.set_text(f'{frequency:.4f}')
        self.num_waves_value_label.set_text(f'{num_waves:.2f}')
        self.modulation_frequency_value_label.set_text(f'{modulation_frequency:.3f}')
        self.line_width_value_label.set_text(f'{line_width}')
        self.rotation_value_label.set_text(f'{rotation:.2f}')

        # Get the color palette
        colors = ColorPalettes.get_palette("neon")
        
        screen = context.screen
        width = screen.get_width()
        height = screen.get_height()
        
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the sine waves with rotation
        center_x, center_y = width // 2, height // 2
        for i in range(num_waves):
            amplitude = base_amplitude - i * amplitude_decrement
            color = colors[i % len(colors)]  # Cycle through the colors
            for x in range(width):
                y = int(height / 2 + amplitude * math.sin(frequency * x + phase_shift))
                rotated_x = int(center_x + (x - center_x) * math.cos(math.radians(rotation)) - (y - center_y) * math.sin(math.radians(rotation)))
                rotated_y = int(center_y + (x - center_x) * math.sin(math.radians(rotation)) + (y - center_y) * math.cos(math.radians(rotation)))
                pygame.draw.line(screen, color, (rotated_x, rotated_y), (rotated_x, rotated_y), line_width)
        
        # handled by the py_wave.py
        # pygame.display.flip()

    def process_event(self, event, manager):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.amplitude_button:
                    self.amplitude_dial = self.toggle_modulation(
                        self.amplitude_dial, (590, 50), 200, (1, 20), manager, 'amplitude'
                    )
                elif event.ui_element == self.frequency_button:
                    self.frequency_dial = self.toggle_modulation(
                        self.frequency_dial, (590, 100), 0.1, (1, 20), manager, 'frequency'
                    )
                elif event.ui_element == self.num_waves_button:
                    self.num_waves_dial = self.toggle_modulation(
                        self.num_waves_dial, (590, 150), 50, (1, 20), manager, 'num_waves'
                    )

        self.update_value_range(self.amplitude_dial, self.amplitude_slider, 10)
        self.update_value_range(self.frequency_dial, self.frequency_slider, 0.001)
        self.update_value_range(self.num_waves_dial, self.num_waves_slider, 1)

def register_design():
    return "Sine Wave", SineWaveDesign()