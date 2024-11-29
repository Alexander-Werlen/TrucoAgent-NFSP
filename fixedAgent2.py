import torch

from classificator2 import Classificator

class FixedAgent:

    def __init__(self, isMano, params):

        if(not torch.cuda.is_available()):
            print("Cuda not available.")
            raise("Cuda not available.")
        self.device = 'cpu' if torch.cuda.is_available() else 'cpu'

        self.isMano = isMano

        #Classification params
        self.MCC_input_layer_size = params["classification_params"]['input_layer_size']
        self.MCC_hidden_layer1_size = params["classification_params"]['hidden_layer1_size']
        self.MCC_hidden_layer2_size = params["classification_params"]['hidden_layer2_size']
        self.MCC_hidden_layer3_size = params["classification_params"]['hidden_layer3_size']
        self.MCC_hidden_layer4_size = params["classification_params"]['hidden_layer4_size']
        self.MCC_output_layer_size = params["classification_params"]['output_layer_size']
        self.MCC_mini_batch_size    = params["classification_params"]['mini_batch_size'] 

        #MCC init
        self.classificator = Classificator(self.MCC_input_layer_size, self.MCC_output_layer_size, self.MCC_hidden_layer1_size, self.MCC_hidden_layer2_size, self.MCC_hidden_layer3_size, self.MCC_hidden_layer4_size).to(self.device)

    def loadAvgPolicy(self, path):
        self.classificator.load_state_dict(torch.load(path, weights_only=True))
    
    def chooseActionWithPolicy(self, state):
        state = torch.tensor(state, dtype=torch.float, device=self.device)
        self.classificator.eval()
        with torch.no_grad():
            actionLogits = self.classificator(state)
            if(actionLogits[0]!=actionLogits[0]): raise("Network output was NAN")
            actionProbabilities = torch.softmax(actionLogits, dim=0)

            chosenIdx = torch.distributions.categorical.Categorical(probs=actionProbabilities).sample().item()
            return chosenIdx
        
    def chooseAction(self, state):
        return self.chooseActionWithPolicy(state)

