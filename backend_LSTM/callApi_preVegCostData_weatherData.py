import requests
import json
import xml.etree.ElementTree as ET
import datetime
import numpy as np
import torch

VegCode_dict = {"絲瓜":"FF1", "花胡瓜":"FD1", "蘿蔔": "SA3", "胡蘿蔔": "SB2", 
                "青蔥": "SE2", "胡瓜":"FC1", "青江白菜": "LD1", "蕹菜(空心菜)": "LF2",
                "甘藍（平地高麗菜）":"LA2", "花椰菜": "FB1", "洋蔥(內銷)": "SD1", "蒜頭": "SG5"}

StationCode_list =["C0F970", "C0X110", "C0U890", "C0T9B0"] # 臺中, 臺南, 宜蘭, 花蓮

def GET_VegCostData(VegCode, StartTime, EndTime): ### GET Veg Pre Cost Data

    url = "https://data.moa.gov.tw/api/v1/AgriProductsTransType"

    data = {"Start_time": StartTime, #112.10.1
            "End_time": EndTime, #112.10.30
            "CropCode": VegCode,   
            "MarketCode": "400"} #400 -> 台中市

    state = requests.get(url, params=data)
    
    return state

def GET_WeatherData(StationID): 

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001"

    data = {"Authorization": "CWB-9F57C6FC-837F-42C0-B434-50A817D87BB2",
            "StationId": StationID} 

    state = requests.get(url, params=data)
    
    return state

def GET_preWeatherData(date): 

    base_url = "https://opendata.cwa.gov.tw/historyapi/v1/getData/O-A0001-001/"
    #date: 2023/12/01/10/00/00"
    data = {"Authorization": "CWB-9F57C6FC-837F-42C0-B434-50A817D87BB2"} 

    state = requests.get(base_url + date, params=data)
    
    return state

def weatherDataGetAndPreproc():
    # get test Weather data
    StationCode_list =["C0F970", "C0X110", "C0U890", "C0T9B0"]

    time_list = [datetime.datetime.now() - datetime.timedelta(days = i) for i in range(1, 11)]

    base_path = "{urn:cwa:gov:tw:cwacommon:0.1}WeatherElement/"

    final_data_list = []
    
    #date: 2023/12/01/10/00/00"
    for i in time_list:
        date_time = f"{i.year}/{i.month:02}/{i.day:02}/23/00/00"
        result = GET_preWeatherData(date_time)
        tree = ET.fromstring(result.text)
        
        data_dict = {}
        date_ = []
        for t in tree.findall("{urn:cwa:gov:tw:cwacommon:0.1}dataset/{urn:cwa:gov:tw:cwacommon:0.1}Station"):
            if(t.find("{urn:cwa:gov:tw:cwacommon:0.1}StationId").text in StationCode_list):
                data_dict[t.find("{urn:cwa:gov:tw:cwacommon:0.1}StationId").text] = \
                [float(t.find(base_path + "{urn:cwa:gov:tw:cwacommon:0.1}Now/{urn:cwa:gov:tw:cwacommon:0.1}Precipitation").text),
                 float(t.find(base_path + "{urn:cwa:gov:tw:cwacommon:0.1}RelativeHumidity").text),
                 float(t.find(base_path + "{urn:cwa:gov:tw:cwacommon:0.1}AirTemperature").text)]

        date_ = sum([data_dict[i] for i in StationCode_list], [])
        final_data_list.append(date_)
    
    final_data_np = np.array(final_data_list)
    final_data_np[final_data_np < 0] = 0.0
    
    return torch.from_numpy(final_data_np)

def vegDataGetAndProc(vegCode):

    time_now = datetime.datetime.now() - datetime.timedelta(days = 1) 
    time_now_format = f"{time_now.year - 1911}.{time_now.month:02}.{time_now.day:02}"
    time_pass = datetime.datetime.now() - datetime.timedelta(days = 65)
    time_pass_format = f"{time_pass.year - 1911}.{time_pass.month:02}.{time_pass.day:02}"

    row_data = GET_VegCostData(vegCode, time_pass_format, time_now_format).json()
    data_ = []
    time_ = []

    for j in range(len(row_data["Data"])):
        data_.append(row_data["Data"][j]["Avg_Price"])
        time_.append(row_data["Data"][j]["TransDate"])

    data_ = data_[::-1]
    time_ = time_[::-1]

    return {"VegData": {"DataLen": len(data_), "Data": data_, "TimeStamp": time_}}

def yesterdayPrecipiation():
    StationCode = "C0F970"

    time = datetime.datetime.now() - datetime.timedelta(days = 1)
    date_time = f"{time.year}/{time.month:02}/{time.day:02}/23/00/00"
    print(date_time)

    base_path = "{urn:cwa:gov:tw:cwacommon:0.1}WeatherElement/"

    result = GET_preWeatherData(date_time)
    tree = ET.fromstring(result.text)

    for t in tree.findall("{urn:cwa:gov:tw:cwacommon:0.1}dataset/{urn:cwa:gov:tw:cwacommon:0.1}Station"):
            if(t.find("{urn:cwa:gov:tw:cwacommon:0.1}StationId").text == StationCode):
                
                result = t.find(base_path + "{urn:cwa:gov:tw:cwacommon:0.1}Now/{urn:cwa:gov:tw:cwacommon:0.1}Precipitation").text
                if(result == "-99"):
                    return 0
                else:
                    return int(result)
 
if __name__ == "__main__":
    ## test Get Veg data

    VegCode_dict = {"絲瓜":"FF1", "花胡瓜":"FD1", "蘿蔔": "SA3", "胡蘿蔔": "SB2", 
                    "青蔥": "SE2", "胡瓜":"FC1", "青江白菜": "LD1", "蕹菜(空心菜)": "LF2",
                    "甘藍（平地高麗菜）":"LA2", "花椰菜": "FB1", "洋蔥(內銷)": "SD1", "蒜頭": "SG5"} 


    print(weatherDataGetAndPreproc())
    #print(yesterdayPrecipiation())
