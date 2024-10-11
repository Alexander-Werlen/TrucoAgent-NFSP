import numpy as np
import random
import torch
from torch import nn
from tqdm import tqdm

from classificator import Classificator
from reservoirMemory import ReservoirMemory

class Test():
    def __init__(self):
        self.iterations = 100000
        self.MCC_learning_rate_a    = 0.5
        self.MCC_mini_batch_size    = 128
        self.MCC_steps_between_optimization  = 128
        self.MCC_input_layer_size = 9
        self.MCC_hidden_layer1_size = 64
        self.MCC_hidden_layer2_size = 64
        self.MCC_hidden_layer3_size = 64
        self.MCC_hidden_layer4_size = 64
        self.MCC_output_layer_size = 4
        self.MCC_reservoir_memory_size = 100000

        self.device = 'cpu'

        random.seed(40)
        self.classificator = Classificator(self.MCC_input_layer_size, self.MCC_output_layer_size, self.MCC_hidden_layer1_size, self.MCC_hidden_layer2_size, self.MCC_hidden_layer3_size, self.MCC_hidden_layer4_size).to(self.device)

        self.memory_mcc = ReservoirMemory(self.MCC_reservoir_memory_size)
        #self.loss_fn_mcc =  nn.BCEWithLogitsLoss()
        self.loss_fn_mcc = nn.CrossEntropyLoss()
        self.optimizer_mcc = torch.optim.SGD(self.classificator.parameters(), lr=self.MCC_learning_rate_a)

        self.step_counter = 0

    def putInMemory(self, state, action):
        self.memory_mcc.append((torch.tensor(state, dtype=torch.float), torch.tensor(action)))

    def generateData(self):
        """ 
        [1,0,0,0,0,0,0,0,0] (0.7, 0) (0.3, 1) 
        [0,1,0,0,0,0,0,0,0] (1, 0)
        [0,0,1,0,0,0,0,0,0] (0.1, 0) (0.9, 1) 

        [1,0,0,0,0,0,1,0,0] (1, 0)
        [0,1,0,0,0,0,1,0,0] (1, 0)
        [0,0,1,0,0,0,1,0,0] (1, 0)

        [1,0,0,0,0,0,0,1,1] (3, 1)
        [0,1,0,0,0,0,0,1,1] (2, 0.5) (3, 0.5)
        [0,0,1,0,0,0,0,1,1] (2, 1) 

        """
        for _ in range(10000):
            idx = random.randint(0,8)
            if(idx==0):
                if(random.random()<0.7):
                    self.putInMemory([1,0,0,0,0,0,0,0,0],0)
                else:
                    self.putInMemory([1,0,0,0,0,0,0,0,0],1)
            elif(idx==1):
                self.putInMemory([0,1,0,0,0,0,0,0,0],0)
            elif(idx==2):
                if(random.random()<0.1):
                    self.putInMemory([0,0,1,0,0,0,0,0,0],0)
                else:
                    self.putInMemory([0,0,1,0,0,0,0,0,0],1)
            elif(idx==3):
                self.putInMemory([1,0,0,0,0,0,1,0,0],0)
            elif(idx==4):
                self.putInMemory([0,1,0,0,0,0,1,0,0],0)
            elif(idx==5):
                self.putInMemory([0,0,1,0,0,0,1,0,0],0)
            elif(idx==6):
                self.putInMemory([1,0,0,0,0,0,0,1,1],3)
            elif(idx==7):
                if(random.random()<0.5):
                    self.putInMemory([0,1,0,0,0,0,0,1,1],2)
                else:
                    self.putInMemory([0,1,0,0,0,0,0,1,1],3)
            elif(idx==8):
                self.putInMemory([0,0,1,0,0,0,0,1,1],2)
            
    def optimize_mcc(self, mini_batch):
        self.classificator.train()

        states, actions= zip(*mini_batch)

        states = torch.stack(states)
        actions = torch.stack(actions)
        actions = torch.tensor([[1.0 if idx==a else 0 for idx in range(self.MCC_output_layer_size)] for a in actions])

        actionsLogits = self.classificator(states)

        loss = self.loss_fn_mcc(actionsLogits, actions)

        # Optimize the model (backpropagation)
        self.optimizer_mcc.zero_grad()  # Clear gradients
        loss.backward()             # Compute gradients
        self.optimizer_mcc.step()       # Update network parameters i.e. weights and biases

    def run(self):
        for _ in tqdm(range((int)(self.iterations/self.MCC_steps_between_optimization*(10/100)))):
            mini_batch = self.memory_mcc.sample(self.MCC_mini_batch_size)
            self.optimize_mcc(mini_batch)

    def getResults(self):
        self.classificator.eval()
        logits = self.classificator(torch.tensor([0,0,1,0,0,0,0,0,0], dtype=torch.float, device="cpu"))
        print("Logits:",logits)
        probs = logits.softmax(dim=0)
        print("Probabilities:",probs)


if __name__ == "__main__":
    test = Test()
    test.generateData()
    test.run()
    test.getResults()