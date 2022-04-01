import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pygame
from keras.layers import Dense, Flatten
from keras.models import Sequential



class Model(Sequential):
    
    op = {
        0: pygame.K_d,
        1: pygame.K_w,
        2: pygame.K_a,
        3: pygame.K_s,
    }
    
    def __init__(self):
        
        super().__init__([
            Flatten(input_shape=(8, 1)),
            Dense(6, activation='relu'),
            Dense(6, activation='relu'),
            Dense(4, activation='softmax')
        ])

        self.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
        
    # def predict(self, x):
    #     return super().predict(x, verbose=0)

    def pred(self, env):
        return list(self.predict( [env] , verbose=0)[0])


    def get_dir(self, env):
        p = self.pred(env)
        # print(f'Right: {dirs[0]}, Up: {dirs[1]}, Left: {dirs[2]}, Down: {dirs[3]}')
        return self.op[p.index(max(p))]


if __name__ == '__main__':
    
    m = Model()
    print(m.summary())
    print(list(m.predict( [ [[1]] * 8 ] )[0]))
    
