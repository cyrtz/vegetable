from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import json

from callApi_preVegCostData_weatherData import vegDataGetAndProc, weatherDataGetAndPreproc, yesterdayPrecipiation
from test_model import test_model, GetWeatherTestDataset

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

VegCode_dict = {"絲瓜":"FF1", "花胡瓜":"FD1", "蘿蔔": "SA3", "胡蘿蔔": "SB2", 
                "青蔥": "SE2", "胡瓜":"FC1", "青江白菜": "LD1", "蕹菜(空心菜)": "LF2",
                "甘藍（平地高麗菜）":"LA2", "花椰菜": "FB1", "洋蔥(內銷)": "SD1", "蒜頭": "SG5"} 

VegName_ = {"絲瓜": "絲瓜", "花胡瓜":  "花胡瓜", "蘿蔔": "蘿蔔", "胡蘿蔔": "胡蘿蔔", 
            "青蔥": "青蔥", "胡瓜": "胡瓜", "青江白菜":  "青江白菜", "空心菜": "蕹菜(空心菜)",
            "高麗菜": "甘藍（平地高麗菜）", "花椰菜": "花椰菜", "洋蔥": "洋蔥(內銷)", "蒜頭": "蒜頭"} 

StationCode_list =["C0F970", "C0X110", "C0U890", "C0T9B0"]

model_path = "./model_file_new/"

@app.route("/GetData", methods=["GET"])
def getData():

    VegName = request.args["VegName"] 
    return_data = vegDataGetAndProc(VegCode_dict[VegName_[VegName]])
    return_data["Pred"] = test_model(f"{model_path}{VegName_[VegName]}train_test.pt", GetWeatherTestDataset())

    return jsonify(return_data)

@app.route("/GetAllVeg", methods=["GET"])
def showAllVeg():
    return_data = {"VegName":list(VegName_.keys())}
    return jsonify(return_data)

@app.route("/CheckStatus", methods=["GET"])
def checkStatus():
    return "True"

@app.route("/getPreDayPrec", methods=["GET"])
def getPreDayPrec():
    return_data = {"YesterdayPrec": yesterdayPrecipiation()}
    return jsonify(return_data)

if __name__ == "__main__":
    app.debug = True
    app.run()
