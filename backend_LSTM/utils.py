import pandas as pd
import json
import numpy as np
import torch 
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np

def get_price_avg(datafarme, dd, commodity):
    _datas = datafarme.loc[datafarme["訪價日期"] == dd][commodity]
    return round(sum(_datas) / len(_datas), 2)

def get_data():
    #price
    price = pd.read_csv("臺中市政府公有零售市場每日蔬果價格表.csv")
    price = pd.DataFrame(price, columns=["市場名稱", "訪價日期", "青蔥"])

    date = set(price["訪價日期"])
    date = list(date)

    price_avg_list = [[], []]
    for i in range(len(date)):
        price_avg_list[0].append(date[i])
        price_avg_list[1].append(get_price_avg(price, date[i], "青蔥"))
        
    new_avg_price = pd.DataFrame(price_avg_list, index=["時間", "青蔥"]).transpose()
    new_avg_price["時間"] = pd.to_numeric(new_avg_price["時間"], downcast="integer")
    new_avg_price = new_avg_price.sort_values(by="時間", ascending=True)

    p = list(new_avg_price["青蔥"])
    d = list(new_avg_price["時間"])

    label = [[d[0]], ["normal"]]

    for i in range(len(p)-1):
        label[0].append(d[i+1])
        if(p[i+1] > p[i]):
            label[1].append("up")
        elif(p[i+1] < p[i]):
            label[1].append("down")
        else:
            label[1].append("normal")
            
    pd_label = pd.DataFrame(label, index=["時間", "標記"]).transpose()

    price_n_label = pd.merge(left=new_avg_price, right=pd_label, how="inner")

    #rain
    f = open("C-B0024-002.json", "r")
    this_year_rain_data = json.load(f)

    #tmp = [[], [], [], [], [], [], [], [], [], []]
    #tmp = [[] for i in range(29)]
    tmp = [[]]
    for i in range(23, 8784, 24):
        tmp[0].append("".join(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][18]["stationObsTimes"]["stationObsTime"][i]["DataTime"][:10].split("-")))

    for j in range(2, 29):
        t = []
        l = len(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][j]["stationObsTimes"]["stationObsTime"])
        if l == 8784:
            for k in range(23, 8784, 24):
                _data = this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][j]["stationObsTimes"]["stationObsTime"][k]["weatherElements"]["Precipitation"]
                if(_data == "T"):
                    _data = 0.1
                t.append(float(_data))
        tmp.append(t)
        """
        tmp[0].append("".join(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][18]["stationObsTimes"]["stationObsTime"][i]["DataTime"][:10].split("-")))
        tmp[1].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][18]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["Precipitation"])
        tmp[2].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][18]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["RelativeHumidity"])
        tmp[3].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][18]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["AirTemperature"])
        tmp[4].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][15]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["Precipitation"])
        tmp[5].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][15]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["RelativeHumidity"])
        tmp[6].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][15]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["AirTemperature"])
        tmp[7].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][11]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["Precipitation"])
        tmp[8].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][11]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["RelativeHumidity"])
        tmp[9].append(this_year_rain_data["cwaopendata"]["resources"]["resource"]["data"]["surfaceObs"]["location"][11]["stationObsTimes"]["stationObsTime"][i]["weatherElements"]["AirTemperature"])

        """
    #rain_data = pd.DataFrame(tmp, index=["時間", "降雨1", "相對濕度1", "氣溫1", "降雨2", "相對濕度2", "氣溫2", "降雨3", "相對濕度3", "氣溫3"]).transpose()
    
    idn = ["時間"] 
    idn.extend(["降雨"+str(i) for i in range(1, len(tmp))])
    rain_data = pd.DataFrame(tmp, index=idn).transpose()
    rain_data["時間"] = pd.to_numeric(rain_data["時間"], downcast="integer")

    mg = pd.merge(left=price_n_label, right=rain_data, how="inner")

    mg = mg.replace("T", 0.1)
    mg = mg.fillna(0.0)

    #np_data = mg.to_numpy()

    #X = np_data[:,3:].astype('float32') #data
    #Y = np_data[:,2] #label

    return mg

class Cget_data():
    def __init__(self):
        super(Cget_data, self).__init__()
        #self.data, self.label = get_data()

    def __new__(self):
        self.data = get_data()
        train = self.data[:-60]
        #test = self.data[-60 - 10:]
        test = self.data[-60:]
        
        train_data = pd.DataFrame()
        test_data = pd.DataFrame()
        
        td = train[train.columns[3:]].to_numpy()
        sd = test[test.columns[3:]].to_numpy()

        """
        td = td.max(axis=1)
        sd = sd.max(axis=1)
        td = train['青蔥']
        sd = test['青蔥']

        for i in range(10):
            train_data[f'c{i}'] = td.tolist()[i: - 10 + i]
            test_data[f'c{i}'] = sd.tolist()[i: - 10 + i]
        """
        
        train_data = []
        test_data = []
        
        for index in range(td.shape[0] - 10):
            train_data.append(td[index: index+10])

        for index in range(sd.shape[0] - 10):
            test_data.append(sd[index: index+10])

        train_label = train['標記'].tolist()[:]
        test_label = test['標記'].tolist()[:]

        #train_label = train['標記'][10:]
        #test_label = test['標記'][10:]

        train_data = np.array(train_data, dtype = "float32")
        test_data = np.array(test_data, dtype = "float32")

        #train_data.astype("float32")
        #print(train_data.shape)
        #train_label, test_data.to_numpy(dtype="float32"), test_label
        #return train_data.to_numpy(dtype="float32"), train_label, test_data.to_numpy(dtype="float32"), test_label
        return train_data, train_label, test_data, test_label

class dataset(Dataset):
    def __init__(self):
        super(dataset, self).__init__()
        self.train_data, self.train_label, self.test_data, self.test_label = Cget_data()
        t_mean = np.mean(self.train_data) 
        t_std = np.std(self.train_data) 
        self.train_data = (self.train_data - t_mean) / t_std

        s_mean = np.mean(self.test_data) 
        s_std = np.std(self.test_data) 
        self.test_data = (self.test_data - s_mean) / s_std

        self.train_data = torch.tensor(self.train_data)
        self.test_data = torch.tensor(self.test_data)
        self.work_type = "train"

        self.LABEL = {"up": torch.tensor(0), "normal": torch.tensor(1), "down": torch.tensor(2)}

    def __getitem__(self, idx):
        if(self.work_type == "train"):
            return self.train_data[idx], (self.LABEL[self.train_label[idx]])
        #return self.train_data[idx], self.train_label[idx]
        if(self.work_type == "test"):
            return self.test_data[idx], (self.LABEL[self.test_label[idx]])
        #return self.test_data[idx], self.test_label[idx]

    def __len__(self):
        if(self.work_type == "train"):
            return len(self.train_data)
        if(self.work_type == "test"):
            return len(self.test_data)
    
    def change_work_type(self, t):
        self.work_type = t 
    
if __name__ == "__main__":
    #Cget_data()
    """
    td, tl, sd, sl = Cget_data()
    print(Cget_data())
    #get_data()
    #print(data)
    #print(label)
    #print(len(data))
    #print(label[0])
    """
    dataset()
    data_ = dataset()
    print(len(data_))
    data_.change_work_type("test")
    print(len(data_))
    print(data_.test_data.shape)
    #print(data_.test_label.count("down"))
