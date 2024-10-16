import numpy as np
import random
import torch
from torch import nn

from dqn import DQN
from replayMemory import ReplayMemory

class GreedyAgent:
    def __init__(self, isMano, params):
        self.lastState = None
        self.lastAction = None
        self.lastActionFollowedEpsilonGreedy = False
        self.isWaitingForFeedback = False

        if(not torch.cuda.is_available()):
            print("Cuda not available.")
            raise("Cuda not available.")
        self.device = 'cpu' if torch.cuda.is_available() else 'cpu'

        self.isMano = isMano
        self.hyperparameter_set = params
        #DQN params
        self.DQN_learning_rate_a    = params["dqn_params"]['learning_rate_a']        # learning rate (alpha)
        self.DQN_discount_factor_g  = params["dqn_params"]['discount_factor_g']      # discount rate (gamma)
        self.DQN_updates_between_target_sync  = params["dqn_params"]['updates_between_target_sync']
        self.DQN_steps_between_optimization  = params["dqn_params"]['steps_between_optimization']
        self.DQN_replay_memory_size = params["dqn_params"]['replay_memory_size']     # size of replay memory
        self.DQN_mini_batch_size    = params["dqn_params"]['mini_batch_size']        # size of the training data set sampled from the replay memory
        self.DQN_epsilon_init       = params["dqn_params"]['epsilon_init']           # 1 = 100% random actions
        self.DQN_epsilon_min        = params["dqn_params"]['epsilon_min']            # minimum epsilon value
        self.DQN_input_layer_size = params["dqn_params"]['input_layer_size']
        self.DQN_hidden_layer1_size = params["dqn_params"]['hidden_layer1_size']
        self.DQN_hidden_layer2_size = params["dqn_params"]['hidden_layer2_size']
        self.DQN_hidden_layer3_size = params["dqn_params"]['hidden_layer3_size']
        self.DQN_hidden_layer4_size = params["dqn_params"]['hidden_layer4_size']
        self.DQN_output_layer_size = params["dqn_params"]['output_layer_size']
        self.DQN_enable_double_dqn  = params["dqn_params"]['enable_double_dqn']    # double dqn on/off flag

        #DQN init        
        self.policy_dqn = DQN(self.DQN_input_layer_size, self.DQN_output_layer_size, self.DQN_hidden_layer1_size, self.DQN_hidden_layer2_size, self.DQN_hidden_layer3_size, self.DQN_hidden_layer4_size).to(self.device)
        self.target_dqn = DQN(self.DQN_input_layer_size, self.DQN_output_layer_size, self.DQN_hidden_layer1_size, self.DQN_hidden_layer2_size, self.DQN_hidden_layer3_size, self.DQN_hidden_layer4_size).to(self.device)
        self.target_dqn.load_state_dict(self.policy_dqn.state_dict())
        
        self.memory_dqn = ReplayMemory(self.DQN_replay_memory_size)
        self.epsilon_dqn = self.DQN_epsilon_init
        self.optimizer_dqn = torch.optim.SGD(self.policy_dqn.parameters(), lr=self.DQN_learning_rate_a)
        self.loss_fn_dqn = nn.MSELoss()
        
        self.step_counter = 0
        self.update_counter = 0

    def chooseActionWithEpsilonGreedy(self):
        self.lastActionFollowedEpsilonGreedy = True
        if(random.random() < self.epsilon_dqn):
            chosenIdx = random.choice(range(self.DQN_output_layer_size))
            self.lastAction = torch.tensor(chosenIdx, dtype=torch.int64, device=self.device)
        else:
            self.policy_dqn.eval()
            with torch.no_grad():
                chosen = self.policy_dqn(self.lastState.unsqueeze(dim=0)).squeeze()
                if(chosen[0]!=chosen[0]): raise("Network output was NAN")
                chosenIdx = chosen.argmax().item()
                self.lastAction = torch.tensor(chosenIdx, dtype=torch.int64, device=self.device)
    

    def chooseAction(self, state):
        self.lastState = torch.tensor(state, dtype=torch.float, device=self.device)

        self.chooseActionWithEpsilonGreedy()

        self.isWaitingForFeedback = True
        self.step_counter += 1
        self.epsilon_dqn = max(self.DQN_epsilon_init/(self.step_counter**0.5), self.DQN_epsilon_min)

        return self.lastAction.item()
    
    def receiveFeedback(self, newState, reward, terminated):
        if(not self.isMano):
            reward = -reward

        newState = torch.tensor(newState, dtype=torch.float, device=self.device)
        reward = torch.tensor(reward, dtype=torch.float, device=self.device)

        #Store transition to replay memory
        self.memory_dqn.append((self.lastState[:], self.lastAction, newState[:], reward, terminated))
        self.lastState = None
        self.lastAction = None
        self.isWaitingForFeedback = False

        #optimize dqn
        if (len(self.memory_dqn)>self.DQN_mini_batch_size and self.step_counter%self.DQN_steps_between_optimization==0):
            mini_batch = self.memory_dqn.sample(self.DQN_mini_batch_size)
            self.optimize_dqn(mini_batch)
            self.update_counter += 1

        
        if (self.update_counter%self.DQN_updates_between_target_sync==0):
            self.target_dqn.load_state_dict(self.policy_dqn.state_dict())
        

    def optimize_dqn(self, mini_batch):
        self.policy_dqn.train()
        self.target_dqn.eval()
        states, actions, new_states, rewards, terminations = zip(*mini_batch)
    
        states = torch.stack(states)

        actions = torch.stack(actions)

        new_states = torch.stack(new_states)

        rewards = torch.stack(rewards)

        terminations = torch.tensor(terminations).float().to(self.device)

        with torch.no_grad():
            if (self.DQN_enable_double_dqn):
                best_actions_from_policy = self.policy_dqn(new_states).argmax(dim=1)

                output = self.target_dqn(new_states).gather(dim=1, index=best_actions_from_policy.unsqueeze(dim=1)).squeeze()

                target_q = rewards + (1-terminations) * self.DQN_discount_factor_g * output
            else:
                # Calculate target Q values (expected returns)
                output = self.target_dqn(new_states).max(dim=1)[0]
                target_q = rewards + (1-terminations) * self.DQN_discount_factor_g * output

        

        # Calcuate Q values from current policy
        current_q = self.policy_dqn(states).gather(dim=1, index=actions.unsqueeze(dim=1)).squeeze()
        # Compute loss
        loss = self.loss_fn_dqn(current_q, target_q)
        # Optimize the model (backpropagation)
        self.optimizer_dqn.zero_grad()  # Clear gradients
        loss.backward()             # Compute gradients
        self.optimizer_dqn.step()       # Update network parameters i.e. weights and biases


    def getIsWaitingForFeedback(self):
        return self.isWaitingForFeedback
    