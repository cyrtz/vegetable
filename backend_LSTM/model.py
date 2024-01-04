import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, x):
        super(Net, self).__init__()
        self.L1 = nn.Linear(x, 100)
        self.L2 = nn.Linear(100, 500)
        self.L3 = nn.Linear(500, 500)
        self.L4 = nn.Linear(500, 100)
        self.L5 = nn.Linear(100, 3)
        
    def forward(self, x):
        x = F.relu(self.L1(x))
        x = F.relu(self.L2(x))
        x = F.relu(self.L3(x))
        x = F.relu(self.L4(x))
        x = F.softmax(self.L5(x), dim=0)

        return x
    
class LSTM_model(nn.Module):
    def __init__(self, input_size=27, hidden_layer_size=8, output_size=3):
        super(LSTM_model, self).__init__()
        self.output_size = output_size
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size, 2, batch_first=True, bidirectional=True) #開 bi 的時候 hidden_layer 要 *2
        self.linear = nn.Linear(hidden_layer_size*2, output_size)
        
    def forward(self, x):
        hidden_cell = (torch.zeros(4, x.size(0), self.hidden_layer_size),
                       torch.zeros(4, x.size(0), self.hidden_layer_size)) 
        output, (hn, cn) = self.lstm(x, hidden_cell)
        output_linear = self.linear(output)
        return output_linear 


