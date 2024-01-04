import pandas as pd
import json
import numpy as np
import torch 
import torch.nn as nn
from torch.utils.data import DataLoader 
import torch.optim as optim
from model import Net, LSTM_model
from utils import dataset
from torchsummary import summary

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
row_data = pd.read_csv("臺中市政府公有零售市場每日蔬果價格表.csv")
pd_row_data = pd.DataFrame(row_data)
veg_list = pd_row_data.columns[2:44].tolist()

def main(veg_, T = True):
    _data = dataset(veg_) 
    if(T == True):
        train_data = DataLoader(_data, batch_size=10, shuffle=True)
        net = LSTM_model(input_size=12)
        net.train()
        net = net.to(device)
        ce = nn.CrossEntropyLoss()
        mse = nn.MSELoss()
        opt = torch.optim.Adam(net.parameters(), lr=0.001)

        #train
        for epoch in range(300):
            running_loss = 0.0
            for batch, d in enumerate(train_data):
                D, L = d
                D = D.to(device)
                L = L.to(device)
                opt.zero_grad()
                result = net(D)
                result = torch.max(result, dim=1).values

                loss = ce(result, L)
                loss.backward()
                opt.step()

                running_loss += loss.item()

            running_loss = 0.0

        torch.save(net, "train_test.pt")
    
    else:
        net = torch.load("./model_file_new/"+str(veg_)+"train_test.pt")
        net = net.to(device)

    net.eval()
    _data.change_work_type("test")
    test_data = DataLoader(_data, batch_size=1, shuffle=True)

    LABEL = ("up", "normal", "down")

    correct_pred = {classname: 0 for classname in LABEL}
    total_pred = {classname: 0 for classname in LABEL}
    #test
    with torch.no_grad():
        for batch, d in enumerate(test_data):
            D, L = d
            D = D.to(device)
            L = L.to(device)
            outputs = net(D)
            nb, predictions = torch.max(outputs, 1)
            nb, predictions = torch.max(nb, 1)
            predictions = predictions.float()

            for label, prediction in zip(L, predictions):
                if label == prediction:
                    correct_pred[LABEL[label]] += 1
                total_pred[LABEL[label]] += 1
    
    for classname, correct_count in correct_pred.items():
        if(correct_count == 0):
            print(f'Accuracy for class: {classname:5s} is 0 %')
            continue
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')

    print(f'Accuracy of the network on the {sum(total_pred.values())} test data: {100 * sum(correct_pred.values()) // sum(total_pred.values())} %')


if __name__ == "__main__":
    net = LSTM_model(input_size=12)
    net.train()
    net = net.to(device)
    model_list = ["絲瓜", 
    "花胡瓜",  
    "蘿蔔",
    "胡蘿蔔",
    "青蔥",
    "胡瓜",
    "青江白菜",
    "蕹菜(空心菜)",
    "甘藍（平地高麗菜）",
    "花椰菜",
    "洋蔥(內銷)",
    "蒜頭"]

    #for i in model_list:
    #    main(i, T=False)

