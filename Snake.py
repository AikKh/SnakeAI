import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from time import sleep, time
import pygame
import numpy as np
from AI import Model
from threading import Thread


class Snake(Thread):
    
    options = {pygame.K_d: (1, 0),
                pygame.K_w: (0, -1),
                pygame.K_a: (-1, 0),
                pygame.K_s: (0, 1)}
    
    life_time = 0
    start_pos = None
    
    training = False
    last = False
    
    def __init__(self, color, cors = 0, dir = pygame.K_d, weights = None):
        super().__init__()
        
        self._dir = dir
        self._cors = [(10, 10 + cors), (9, 10 + cors), (8, 10 + cors), (7, 10 + cors), (6, 10 + cors)]
        self.start_pos = self._cors.copy()
        
        self._head = self._cors[0]
        self._size = len(self._cors)
        self._color = color
        self._current_apple = [(14, 10), (14, 15), (14, 20)]
        
        
        self._model = Model()
        
        if weights != None:
            self._model.set_weights(weights)
        
        # with open('test.npy', 'rb') as f:
        #     weights = np.load(f, allow_pickle=True)
        self._die = False
        
        self.start()
                
        
    def move(self):
        x, y = self.options[self._dir]
        
        old_one = self._cors[0]
        self._cors[0] = (self._cors[0][0] + x, self._cors[0][1] + y)
        for i in range(1, self._size):
            self._cors[i], old_one = old_one, self._cors[i]
            
        self._head = self._cors[0]

            
    def eat(self, apple_cors):
        x, y = self.options[self._dir]
        self._cors.append((self._cors[-1][0] + x, self._cors[-1][0] + y))
        self._size += 1
        self._current_apple = apple_cors
      
      
    def get_env(self):
        hx, hy = self._head
        def get_place_by_cor(x, y):
            if not (0 < x <= 60 and 0 < y <= 60) or (x, y) in self._cors[1:]:
                return 1
            elif (x, y) in self._current_apple:
                return 2
            return 0
        
        env = [(hx + x, hy + y) for x in range(-1, 2, 1) for y in range(-1, 2, 1) if (x, y) != (0, 0)]
        return [[get_place_by_cor(x, y)] for x, y in env]
    
    
      
    def run(self):
        head = tuple(self._head)
        start = time()
        while not self._die:
            if head != self._head:
                env = self.get_env()
                self._dir = self._model.get_dir(env)
                head = self._head
                
                
        self.life_time = time() - start
        print(f'Time: {self.life_time}')
        
        