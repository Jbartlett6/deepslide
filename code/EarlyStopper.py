import math

class EarlyStopper():
    '''
    Simple early stopping class to be included in a training loop. The class
    takes threshold as input which is the number of updates without improvement 
    before early stopping takes place. When the EarlyStopper has been updated 
    more than threshold number of times without improvement the indicator
    attribute changes from False to True. At this point training should stop. 
    the indicator must be checked in the training loop..
    '''
    def __init__(self, threshold):
        self.threshold = threshold
        self.best_loss = math.inf 
        self.indicator = False
        self.steps_since_improvement = 0

    def update(self, loss):
        if self.indicator == False:
            if (loss < self.best_loss):
                self.best_loss = loss
                self.steps_since_improvement = 0
            else:
                self.steps_since_improvement += 1
                if self.steps_since_improvement > self.threshold:
                    self.indicator == True
        print(f'''EarlyStopper Updated: \n
              Steps since improvement: {self.steps_since_improvement} \n
              Best loss: {self.best_loss}
              ''')
        