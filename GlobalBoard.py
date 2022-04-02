import pygame

WHITE = 255, 255, 255
BLACK = 40, 40, 40

PIX = 10

pygame.init()
width = height = 60*PIX
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("SnakeAI")

clock = pygame.time.Clock()
fps = 10

def draw(*cors, color):
    for x, y in cors:
        pygame.draw.rect(screen, color, (x*PIX, y*PIX, PIX, PIX))