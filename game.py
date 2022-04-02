#main
from time import sleep
import pygame
import random
from Snake import Snake
import numpy as np
from AI import Model


WHITE = 255, 255, 255
BLACK = 0, 0, 0
PIX = 10

RUNNING = True
GENERATION = 1

COLORS = []
        
class Board:
       
    pygame.init()
    width = height = 59*PIX
    screen = pygame.display.set_mode((width, height))
    
    pygame.display.set_caption("SnakeAI")
    
    clock = pygame.time.Clock()
    fps = 10

    def __init__(self):
        self._snakes = [Snake((255, 128, 0)),
                        Snake((0, 0, 255), cors=5), 
                        Snake((0, 255, 0), cors=10)]
        
        
    def snakeDecorator(func): 
        def decorator(self):
            for snake in self._snakes:
                func(self, snake)
                
        return decorator
    
        
    @snakeDecorator
    def draw(self, snake: Snake):
        if not snake._die:
            pygame.draw.rect(self.screen, (255, 0, 0), (snake._apple[0]*PIX, snake._apple[1]*PIX, PIX, PIX))
            for x, y in snake._cors:
                pygame.draw.rect(self.screen, snake._color, (x*PIX, y*PIX, PIX, PIX))
        
    
                        
    def main(self):
        global GENERATION
        print('GENERATION:', GENERATION)
        
        while sum([not snake._die for snake in self._snakes]) > 0:
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.draw()
            
            self.clock.tick(self.fps)
       
           
        last_snake = self._snakes[0]
        for snake in self._snakes[1:]:
            if snake.life_time > last_snake.life_time or snake._size > last_snake._size:
                last_snake = snake

        weights = last_snake._model.get_weights()
        
        # with open(f'Generation-{GENERATION}.npy', 'wb') as f:
        #     np.save(f, np.array(weights, dtype=np.ndarray))
        
         
        self._snakes = [
            Snake((255, 128, 0), weights=Model.getChangeWeights(weights)), 
            Snake((0, 0, 255), cors=5, weights=Model.getChangeWeights(weights)), 
            Snake((0, 255, 0), cors=10, weights=Model.getChangeWeights(weights)),
        ]
        
        GENERATION += 1
        return self.main()
            
                        
game = Board()
game.main()

        