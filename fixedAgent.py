import torch

from classificator import Classificator

class FixedAgent:

    def __init__(self, isMano, params):

        if(not torch.cuda.is_available()):
            print("Cuda not available.")
            raise("Cuda not available.")
        self.device = 'cpu' if torch.cuda.is_available() else 'cpu'

        self.isMano = isMano
        self.hyperparameter_set = params

        #Classification params
        self.MCC_learning_rate_a    = params["classification_params"]['learning_rate_a']
        self.MCC_steps_between_optimization  = params["classification_params"]['steps_between_optimization']
        self.MCC_input_layer_size = params["classification_params"]['input_layer_size']
        self.MCC_hidden_layer1_size = params["classification_params"]['hidden_layer1_size']
        self.MCC_hidden_layer2_size = params["classification_params"]['hidden_layer2_size']
        self.MCC_hidden_layer3_size = params["classification_params"]['hidden_layer3_size']
        self.MCC_hidden_layer4_size = params["classification_params"]['hidden_layer4_size']
        self.MCC_output_layer_size = params["classification_params"]['output_layer_size']
        self.MCC_reservoir_memory_size = params["classification_params"]['reservoir_memory_size']
        self.MCC_mini_batch_size    = params["classification_params"]['mini_batch_size'] 

        #MCC init
        self.classificator = Classificator(self.MCC_input_layer_size, self.MCC_output_layer_size, self.MCC_hidden_layer1_size, self.MCC_hidden_layer2_size, self.MCC_hidden_layer3_size, self.MCC_hidden_layer4_size).to(self.device)

    def loadAvgPolicy(self, path):
        self.classificator.load_state_dict(torch.load(path, weights_only=True))
    
    def chooseActionWithPolicy(self, state ,validityOfActions):
        state = torch.tensor(state, dtype=torch.float, device=self.device)
        with torch.no_grad():
            actionLogits = self.classificator(state)
            actionProbabilities = torch.softmax(actionLogits, dim=0)
            for i in range(self.MCC_output_layer_size):
                if(not validityOfActions[i]): actionProbabilities[i] = 0

            chosenIdx = torch.distributions.categorical.Categorical(probs=actionProbabilities).sample().item()
            return chosenIdx

