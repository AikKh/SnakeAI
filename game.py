from Snake import Snake
import numpy as np
from AI import Model


GENERATION = 1

class Game:
       
    def __init__(self):
        self._colors = [(132, 20, 106), (159, 69, 75), (221, 179, 140), 
                        (147, 100, 81), (255, 128, 0), (148, 4, 148),
                        (45, 117, 96), (29, 129, 241), (88, 66, 86),
                        (132, 149, 117), (92, 63, 219), (214, 17, 42),
                        (101, 92, 209), (233, 32, 20), (22, 243, 72)]
        
        self._snakes = [Snake(rgb) for rgb in self._colors]
        
        
    def main(self):
        global GENERATION
        print('GENERATION:', GENERATION)
        
        for snake in self._snakes:
            snake.start()
            snake.join()
       
           
        last_snake = self._snakes[0]
        for snake in self._snakes[1:]:
            if snake.points > last_snake.points:
                last_snake = snake

        weights = last_snake._model.get_weights()
        
        # with open(f'Generations/Generation-{GENERATION}.npy', 'wb') as f:
        #     np.save(f, np.array(weights, dtype=np.ndarray))
        
         
        self._snakes = [Snake(rgb, weights=Model.getChangeWeights(weights)) for rgb in self._colors]
        
        GENERATION += 1
        return self.main()
            
                        
game = Game()
game.main()


        