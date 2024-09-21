from base_design import BaseDesign
import pygame

class Design1(BaseDesign):
    def register_design(self):
        return "Design 1", self.draw_design

    def draw_design(self, screen, font, frame):
        screen.fill((0, 0, 0))
        text = font.render(f'Py-Wave Frame: {frame}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

def register_design():
    return Design1().register_design()

