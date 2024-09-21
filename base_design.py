import pygame

class BaseDesign:
    def init(self, manager):
        """Initialize any GUI elements or other resources."""
        pass

    def uninit(self):
        """Clean up any GUI elements or other resources."""
        pass

    def draw_design(self, context):
        screen = context.screen
        font = context.font
        frame = context.frame
        
        screen.fill((0, 0, 0))
        text = font.render(f'Py-Wave Frame: {frame}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        
    def process_event(self, event, manager):
        '''Process any events, such as key presses.'''
        pass