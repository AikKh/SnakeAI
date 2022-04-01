from time import sleep
import pygame
import random
from Snake import Snake
import numpy as np


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
    fps = 6

    eat = 0
    
    def __init__(self):
        self._snakes = [Snake((255, 128, 0)),
                        Snake((0, 0, 255), cors=5), 
                        Snake((0, 255, 0), cors=10)]
        
        self._apple_cors = self.appleGrowUp()
        
    
    def snakeDecorator(func): 
        def decorator(self):
            for snake in self._snakes:
                func(self, snake)
                
        return decorator
    
    
    def appleGrowUp(self):
    
        free_space = [(x, y) for x in range(60) for y in range(60) if (x, y) not in [snake_cors for snake in self._snakes for snake_cors in snake._cors]]
        return free_space.pop(random.randrange(len(free_space)))
        
        
    @snakeDecorator
    def draw(self, snake: Snake):
        if not snake._die:
            for x, y in snake._cors:
                pygame.draw.rect(self.screen, snake._color, (x*PIX, y*PIX, PIX, PIX))
        
    @snakeDecorator
    def allMove(self, snake: Snake):
        if not snake._die:
            snake.move()
        # for commit
    def allDieCheck(self):
        for snake in self._snakes:
            if not snake._die:
                return False
        return True
    
            
    @snakeDecorator  
    def snakeAlive(self, snake: Snake):
        global RUNNING
        
        h = snake._head
        if not (0 <= h[0] < 60 and 0 <= h[1] < 60) or h in snake._cors[1:]:
            snake._die = True
            
            if self.allDieCheck():
                RUNNING = False
                
        elif h in self._apple_cors:
            self.eat += 1
            self._apple_cors = self.appleGrowUp()
            snake.eat(self._apple_cors)
    
    
    def changeWeights(self, arrey: list):
        new_arrey = arrey.copy()

        for l in [0, 2, 4]:
            for y in range(len(new_arrey[l])):
                for x in range(len(new_arrey[l][y])):
                    new_arrey[l][y][x] += (random.randrange(-10, 11)) / 10
                    
        return new_arrey
        
                        
    def main(self):
        global RUNNING, GENERATION
        print('GENERATION:', GENERATION)
            
        while RUNNING:
            pygame.display.flip()
            self.screen.fill(BLACK)
            self.draw()
            for apple in self._apple_cors:
                pygame.draw.rect(self.screen, (255, 0, 0), (apple[0] * PIX, apple[1] * PIX, PIX, PIX))
            
            self.allMove()
            self.snakeAlive()
            self.clock.tick(self.fps)
       
           
        last_snake = self._snakes[0]
        for snake in self._snakes[1:]:
            if snake.life_time > last_snake.life_time or snake._size > last_snake._size:
                last_snake = snake
            

        weights = last_snake._model.get_weights()
        
        # with open(f'Generation-{GENERATION}.npy', 'wb') as f:
        #     np.save(f, np.array(weights, dtype=np.ndarray))
        
         
        self._snakes = [
            Snake((255, 128, 0), weights=self.changeWeights(weights)), 
            Snake((0, 0, 255), cors=5, weights=self.changeWeights(weights)), 
            Snake((0, 255, 0), cors=10, weights=self.changeWeights(weights)),
        ]
        
        self._apple_cors = self.appleGrowUp()
        RUNNING = True
        GENERATION += 1
        return self.main()
            
                        
game = Board()
game.main()

        