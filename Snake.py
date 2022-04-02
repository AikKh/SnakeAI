import os, random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from time import sleep, time
import pygame
import numpy as np
from AI import Model
from threading import Thread


class Snake(Thread):
    
    
    life_time = 0
    start_pos = None
    
    training = False
    last = False
    
    clock = pygame.time.Clock()
    fps = 10
    
    def __init__(self, color, cors = 0, dir = pygame.K_d, weights = None):
        super().__init__()
        
        self._dir = dir
        self._cors = [(10, 10 + cors), (9, 10 + cors), (8, 10 + cors), (7, 10 + cors), (6, 10 + cors)]
        self.start_pos = self._cors.copy()
        
        self._head = self._cors[0]
        self._size = len(self._cors)
        self._color = color
        self._apple = self.appleGrowUp()
        
        
        self._model = Model()
        
        if weights != None:
            self._model.set_weights(weights)
        
        # with open('test.npy', 'rb') as f:
        #     weights = np.load(f, allow_pickle=True)
        self._die = False
        
        self.start()
                
        
    def move(self):
        x, y = self._dir
        
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
        h = self._head
        if not (0 <= h[0] < 60 and 0 <= h[1] < 60) or h in self._cors[1:]:
            self._die = True
            
        elif h == self._apple:
            self._apple_cors = self.appleGrowUp()
            self.eat()
      
      
    def getEnv(self):
        hx, hy = self._head
        def getPlaceByCor(x, y):
            if not (0 < x <= 60 and 0 < y <= 60) or (x, y) in self._cors[1:]:
                return 0
            elif (x, y) in self._apple:
                return 20
            return 1
        
        rng = range(-1, 2, 1)
        env = [(hx + x, hy + y) for x in rng for y in rng if (x, y) != (0, 0)]
        return [[getPlaceByCor(x, y)] for x, y in env]
    
    
      
    def run(self):
        start = time()
        while not self._die:
            env = self.getEnv()
            self._dir = self._model.getDir(env)
            self.move()
            self.isAlive()
            self.clock.tick(self.fps)
                
                
        self.life_time = time() - start
        print(f'Time: {self.life_time}')
        
        