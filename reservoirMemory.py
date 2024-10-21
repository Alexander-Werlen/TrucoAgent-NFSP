from collections import deque
import random

class ReservoirMemory:

    def __init__(self, maxlen, minProbOfReplacement):
        self.streamLength = 0
        self.maxlen = maxlen
        self.minProbOfReplacement = minProbOfReplacement
        self.memory = deque([], maxlen=maxlen)

    def append(self, transition):
        self.streamLength += 1

        if(len(self.memory) == self.maxlen-1):
            print("Reservoir memory full")

        if(len(self.memory) < self.maxlen):
            self.memory.append(transition)
        else:
            p = max(self.minProbOfReplacement,self.maxlen/self.streamLength)
            if(random.random() < p):
                self.memory[random.randrange(self.maxlen)] = transition

    def sample(self, sample_size):
        return random.sample(self.memory, sample_size)

    def __len__(self):
        return len(self.memory)
    
    def show(self):
        print(self.memory)