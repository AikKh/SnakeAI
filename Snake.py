import os, random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import glob
import numpy as np
import pygame
from time import time
from AI import Model
from threading import Thread
from GlobalBoard import clock, fps, screen, draw, BLACK


class Snake(Thread):
    
    
    points = 0
    
    clock = pygame.time.Clock()
    fps = 10
    
    def __init__(self, color, weights = None):
        super().__init__()
        
        self._dir = pygame.K_d
        self._cors = [(30, 30), (29, 30), (28, 30), (27, 30), (26, 30)]
        
        self._head = self._cors[0]
        self._size = len(self._cors)
        self._color = color
        self._apple = self.appleGrowUp()#(32, 30)
        
        self._observe = 5
        self._model = Model(self._observe)
        
        if weights is not None:
            self._model.set_weights(weights)
        # else:
        #     list_of_files = glob.glob('Generations/*')
        #     latest_file = max(list_of_files, key=os.path.getctime)

        #     weights = np.load(latest_file, allow_pickle=True)
            
        #     # os.rename(latest_file, 'Generations\\Generation-0.npy')
        #     for filename in os.listdir("Generations")[:-1]:
        #         filename_relPath = os.path.join("Generations", filename)
        #         os.remove(filename_relPath)

        self._die = False
        
        
    def move(self):
        x, y = self._dir
        self.points += self._size
        
        old_one = self._cors[0]
        self._cors[0] = (self._cors[0][0] + x, self._cors[0][1] + y)
        for i in range(1, self._size):
            self._cors[i], old_one = old_one, self._cors[i]
            
        self._head = self._cors[0]

            
    def eat(self):
        x, y = self._dir
        self._cors.append((self._cors[-1][0] + x, self._cors[-1][0] + y))
        self._size += 1
        self._apple = self.appleGrowUp()
        
        
    def appleGrowUp(self):
        free_space = [(x, y) for x in range(60) for y in range(60) if (x, y) not in self._cors]
        return random.choice(free_space)
        
        
    def isAlive(self):
        hx, hy = self._head
        if not (0 <= hx < 60 and 0 <= hy < 60) or (hx, hy) in self._cors[1:]:
            self._die = True
            
        elif (hx, hy) == self._apple:
            self._apple_cors = self.appleGrowUp()
            self.eat()
      
      
    def getEnv(self):
        hx, hy = self._head
        def getPlaceByCor(x, y):
            if not (0 < x <= 60 and 0 < y <= 60) or (x, y) in self._cors[1:]:
                return 0
            elif (x, y) == self._apple:
                return 2
            return 1
        
        rng = range(-self._observe, self._observe + 1)
        return [[getPlaceByCor(hx + x, hy + y) for x in rng] for y in rng]
        
      
    def run(self):
        start = time()
        while not self._die:
            self._dir = self._model.getDir(self.getEnv())
            self.move()
            self.isAlive()
            draw(*self._cors, self._apple, color=self._color)
            clock.tick(fps)
            pygame.display.flip()
            screen.fill(BLACK)
                
                
        life_time = time() - start
        print(f'Time: {life_time}')
        
if __name__ == '__main__':
    snake = Snake((0, 0, 0))
    for i in snake.getEnv():
        print(i)
        
        