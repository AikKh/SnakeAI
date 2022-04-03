import pygame

WHITE = 255, 255, 255
BLACK = 40, 40, 40

pygame.init()
width = height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("SnakeAI")

clock = pygame.time.Clock()
fps = 10

def draw(*cors:tuple[tuple[int, int]], color: tuple[int, int, int], pix: int = 10):
    for x, y in cors:
        pygame.draw.rect(screen, color, (x*pix, y*pix, pix, pix))