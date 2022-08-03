import pygame

class Text:

    def __init__(self, text, pos, color, background=None):
        pygame.font.init()
        self.pos = pos
        self.font = pygame.font.Font("Rainshow.otf", 32)
        self.text = self.font.render(text, True, color, background)
        self.rect = self.text.get_rect()
        self.rect.center = pos


    def write(self, screen : pygame.display):
        screen.blit(self.text, self.rect)
