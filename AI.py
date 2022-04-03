import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import random
import pygame
from keras.layers import Dense, Flatten
from keras.models import Sequential



class Model(Sequential):
    
    op = [(1, 0), (0, -1),(-1, 0),(0, 1)]
    
    
    def __init__(self, observe):
        
        observe = 2 * observe + 1
        
        super().__init__([
            Flatten(input_shape=(observe, observe)),
            # Dense(6, activation='relu'),
            Dense(6, activation='relu'),
            Dense(4, activation='softmax')
        ])

        self.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
        

    def pred(self, env):
        return list(self.predict( [env] , verbose=0)[0])


    def getDir(self, env):
        p = self.pred(env)
        return self.op[p.index(max(p))]

    
    @staticmethod
    def getChangeWeights(arrey: list):
        new_arrey = arrey.copy()

        for l in [0, 2]:
            for y in range(len(new_arrey[l])):
                for x in range(len(new_arrey[l][y])):
                    new_arrey[l][y][x] += (random.randrange(-10, 11) / 10)
                    
        return new_arrey


if __name__ == '__main__':
    
    m = Model()
    print(m.summary())
    print(list(m.predict( [ [[1]] * 8 ] )[0]))
    
