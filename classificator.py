import torch
from torch import nn
import torch.nn.functional as F

class Classificator(nn.Module):

    def __init__(self, state_dim, action_dim, hidden_dim1, hidden_dim2, hidden_dim3, hidden_dim4):
        super(Classificator, self).__init__()

        self.fc1 = nn.Linear(state_dim, hidden_dim1)
        self.fc2 = nn.Linear(hidden_dim1, hidden_dim2)
        self.fc3 = nn.Linear(hidden_dim2, hidden_dim3)
        self.fc4 = nn.Linear(hidden_dim3, hidden_dim4)
        self.output = nn.Linear(hidden_dim4, action_dim)

    def forward(self, x):
        x1 = F.relu(self.fc1(x))
        x2 = F.relu(self.fc2(x1))
        x3 = F.relu(self.fc3(x2))
        x4 = F.relu(self.fc4(x3))
        return self.output(x4)