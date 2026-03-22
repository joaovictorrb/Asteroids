import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 50)

    def draw(self):
        self.screen.fill("black")

        title = self.font.render("Asteroids", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        self.screen.blit(title, title_rect)

        start_text = self.font_small.render("Start Game (Press Enter)", True, TEXT_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(start_text, start_rect)
