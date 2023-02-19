#!/usr/bin/python
# -*- coding: <UTF-8> -*-

"""
Main flask application containing routing URL´s.
"""


import json
import os

import numpy as np
import toml
from flask import Flask, jsonify, render_template, request

app = Flask(__name__,template_folder='template')

from openpyxl import load_workbook


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/next')
def main():
    global userData
    cwd = os.getcwd()
    print(cwd)

    #userData = toml.load(r"C:/Users/sathi/Desktop/repos/MA-Aanand-Turbulence/visualization/userData.toml")
    #userData = toml.load("repos/MA-Aanand-Turbulence/visualization/userData.toml")
    userData = toml.load("/home/satish/thesis/flask/repos/MA-Aanand-Turbulence/visualization/userData.toml")
   
   
    return render_template('visualizations.html',datasets=userData.keys())

@app.route('/available')
def avail():

    return render_template('available.html')

@app.route("/dimRed", methods=["POST"])
def dimRed():
    global data, userData

    parameters = request.get_json()
    dataset = parameters["dataset"]
    print('Dataset name {0}'.format(dataset))
    
    #3 ts
    if(dataset==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3")):
    # read json file
        with open(userData[dataset]) as f:
            data = json.load(f)

        return jsonify({
                
                "seqlength":data["seqlength"],
                "time_increment":data["time_increment"],
                "accuracy": data["model_accuracy"],
                "hiddenStatesgru": data["hsoutputhiddenstates"],
                "gruweights": data["gruweights"],
                "zerohidden":data["zerohidden"],
                "hiddenStatesreshape": data["hiddenstates"],
                "hiddenstateo":data["hiddenstateso"],
                "testinputs": data["test_input"],
                "actualValues": data["test_output"],
                "predictions": data["prediction"],
                "pcaprojection":data["pcaprojection"],
                "projection": data["projection"],
                "nfeatures": data["nfeatures"],
                "projectiono": data["projectiono"],
                #"mdsprojection":data["mdsprojection"],
                "umapprojection":data["umapprojection"],

                "c0":data["c0"],
                "c1":data["c1"],
                "c2":data["c2"],

                "co0":data["co0"],
                "co1":data["co1"],
                "co2":data["co2"]
                
                
                })
    #5ts
    if(dataset==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3")):
    # read json file
        with open(userData[dataset]) as f:
            data = json.load(f)
        
            
        return jsonify({
                
                "seqlength":data["seqlength"],
                "time_increment":data["time_increment"],
                "accuracy": data["model_accuracy"],
                "hiddenStatesgru": data["hsoutputhiddenstates"],
                "gruweights": data["gruweights"],
                "zerohidden":data["zerohidden"],
                "hiddenStatesreshape": data["hiddenstates"],
                "hiddenstateo":data["hiddenstateso"],
                "testinputs": data["test_input"],
                "actualValues": data["test_output"],
                "predictions": data["prediction"],
                "pcaprojection":data["pcaprojection"],
                "projection": data["projection"],
                "nfeatures": data["nfeatures"],
                "projectiono": data["projectiono"],
                #"mdsprojection":data["mdsprojection"],
                "umapprojection":data["umapprojection"],

                "c0":data["c0"],
                "c1":data["c1"],
                "c2":data["c2"],
                "c3":data["c3"],
                "c4":data["c4"],

                "co0":data["co0"],
                "co1":data["co1"],
                "co2":data["co2"],
                "co3":data["co3"],
                "co4":data["co4"]
                
                })

    #10ts 
    if(dataset==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3")):
    # read json file
        with open(userData[dataset]) as f:
            data = json.load(f)

        return jsonify({
                
                "seqlength":data["seqlength"],
                "time_increment":data["time_increment"],
                "accuracy": data["model_accuracy"],
                "hiddenStatesgru": data["hsoutputhiddenstates"],
                "gruweights": data["gruweights"],
                "zerohidden":data["zerohidden"],
                "hiddenStatesreshape": data["hiddenstates"],
                "hiddenstateo":data["hiddenstateso"],
                "testinputs": data["test_input"],
                "actualValues": data["test_output"],
                "predictions": data["prediction"],
                "pcaprojection":data["pcaprojection"],
                "projection": data["projection"],
                "nfeatures": data["nfeatures"],
                "projectiono": data["projectiono"],
                #"mdsprojection":data["mdsprojection"],
                "umapprojection":data["umapprojection"],

                "c0":data["c0"],
                "c1":data["c1"],
                "c2":data["c2"],
                "c3":data["c3"],
                "c4":data["c4"],
                "c5":data["c5"],
                "c6":data["c6"],
                "c7":data["c7"],
                "c8":data["c8"],
                "c9":data["c9"],

                "co0":data["co0"],
                "co1":data["co1"],
                "co2":data["co2"],
                "co3":data["co3"],
                "co4":data["co4"],
                "co5":data["co5"],
                "co6":data["co6"],
                "co7":data["co7"],
                "co8":data["co8"],
                "co9":data["co9"]
                
                })
    #20ts
    if(dataset==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3")):
    # read json file
         with open(userData[dataset]) as f:
            data = json.load(f)

         return jsonify({
                
                "seqlength":data["seqlength"],
                "time_increment":data["time_increment"],
                "accuracy": data["model_accuracy"],
                "hiddenStatesgru": data["hsoutputhiddenstates"],
                "gruweights": data["gruweights"],
                "zerohidden":data["zerohidden"],
                "hiddenStatesreshape": data["hiddenstates"],
                "hiddenstateo":data["hiddenstateso"],
                "testinputs": data["test_input"],
                "actualValues": data["test_output"],
                "predictions": data["prediction"],
                "pcaprojection":data["pcaprojection"],
                "projection": data["projection"],
                "nfeatures": data["nfeatures"],
                "projectiono": data["projectiono"],
                #"mdsprojection":data["mdsprojection"],
                "umapprojection":data["umapprojection"],

                "c0":data["c0"],
                "c1":data["c1"],
                "c2":data["c2"],
                "c3":data["c3"],
                "c4":data["c4"],
                "c5":data["c5"],
                "c6":data["c6"],
                "c7":data["c7"],
                "c8":data["c8"],
                "c9":data["c9"],
                "c10":data["c10"],
                "c11":data["c11"],
                "c12":data["c12"],
                "c13":data["c13"],
                "c14":data["c14"],
                "c15":data["c15"],
                "c16":data["c16"],
                "c17":data["c17"],
                "c18":data["c18"],
                "c19":data["c19"],

                "co0":data["co0"],
                "co1":data["co1"],
                "co2":data["co2"],
                "co3":data["co3"],
                "co4":data["co4"],
                "co5":data["co5"],
                "co6":data["co6"],
                "co7":data["co7"],
                "co8":data["co8"],
                "co9":data["co9"],
                "co10":data["co10"],
                "co11":data["co11"],
                "co12":data["co12"],
                "co13":data["co13"],
                "co14":data["co14"],
                "co15":data["co15"],
                "co16":data["co16"],
                "co17":data["co17"],
                "co18":data["co18"],
                "co19":data["co19"]
                
                })
    #else:
        #return render_template('error1.html')
    
@app.route('/comparison')
def compare():
    global userData

    cwd = os.getcwd()
    print(cwd)

    userData = toml.load("/home/satish/thesis/flask/repos/MA-Aanand-Turbulence/visualization/userData.toml")

    return render_template('comparison.html',datasets=userData.keys())

@app.route("/comparing", methods=["POST"])
def comparing():
    global data1,data2, userData
    

    
    parameters= request.get_json()
    print('parameters name {0}'.format(parameters))
    print('parameters type {0}'.format(type(parameters)))
    
    dataset1 = parameters["dataset1"]
    dataset2 = parameters["dataset2"]
    print('Dataset1 name {0}'.format(dataset1))
    print('Dataset2 name {0}'.format(dataset2))
    
    #3 ts 3ts
    if( (dataset1==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3") )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "hiddenStatesgru1": data1["hsoutputhiddenstates"],
                "gruweights1": data1["gruweights"],
                "zerohidden1":data1["zerohidden"],
                "hiddenStatesreshape1": data1["hiddenstates"],
                "hiddenstateo1":data1["hiddenstateso"],
                "testinputs1": data1["test_input"],
                "actualValues1": data1["test_output"],
                "predictions1": data1["prediction"],
                "pcaprojection1":data1["pcaprojection"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                "projectiono1": data1["projectiono"],
                "umapprojection1":data1["umapprojection"],

                "c01":data1["c0"],
                "c11":data1["c1"],
                "c21":data1["c2"],

                "co01":data1["co0"],
                "co11":data1["co1"],
                "co21":data1["co2"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "hiddenStatesgru2": data2["hsoutputhiddenstates"],
                "gruweights2": data2["gruweights"],
                "zerohidden2":data2["zerohidden"],
                "hiddenStatesreshape2": data2["hiddenstates"],
                "hiddenstateo2":data2["hiddenstateso"],
                "testinputs2": data2["test_input"],
                "actualValues2": data2["test_output"],
                "predictions2": data2["prediction"],
                "pcaprojection2":data2["pcaprojection"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                "projectiono2": data2["projectiono"],
                "umapprojection2":data2["umapprojection"],

                "c02":data2["c0"],
                "c12":data2["c1"],
                "c22":data2["c2"],

                "co02":data2["co0"],
                "co12":data2["co1"],
                "co22":data2["co2"]
                
                
                })

    #5 ts 5ts
    if( (dataset1==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3"))):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],

                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],

                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })
    #10 ts 
    if( (dataset1==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3"))):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
 
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],

                })
    
     #20 ts 20ts
    if( (dataset1==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3"))):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                 
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],


                })

    #3 ts 5ts
    if( (dataset1==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3") )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "hiddenStatesgru1": data1["hsoutputhiddenstates"],
                "gruweights1": data1["gruweights"],
                "zerohidden1":data1["zerohidden"],
                "hiddenStatesreshape1": data1["hiddenstates"],
                "hiddenstateo1":data1["hiddenstateso"],
                "testinputs1": data1["test_input"],
                "actualValues1": data1["test_output"],
                "predictions1": data1["prediction"],
                "pcaprojection1":data1["pcaprojection"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                "projectiono1": data1["projectiono"],
                "umapprojection1":data1["umapprojection"],

                "c01":data1["c0"],
                "c11":data1["c1"],
                "c21":data1["c2"],

                "co01":data1["co0"],
                "co11":data1["co1"],
                "co21":data1["co2"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                
                })

     #3 ts 10ts
    if( (dataset1==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3") )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "hiddenStatesgru1": data1["hsoutputhiddenstates"],
                "gruweights1": data1["gruweights"],
                "zerohidden1":data1["zerohidden"],
                "hiddenStatesreshape1": data1["hiddenstates"],
                "hiddenstateo1":data1["hiddenstateso"],
                "testinputs1": data1["test_input"],
                "actualValues1": data1["test_output"],
                "predictions1": data1["prediction"],
                "pcaprojection1":data1["pcaprojection"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                "projectiono1": data1["projectiono"],
                "umapprojection1":data1["umapprojection"],

                "c01":data1["c0"],
                "c11":data1["c1"],
                "c21":data1["c2"],

                "co01":data1["co0"],
                "co11":data1["co1"],
                "co21":data1["co2"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })

     #3 ts 20ts
    if( (dataset1==("turbulence31_s3tsep10bs128lr0.01af1") or  ("turbulence32_s3tsep10bs128lr0.01af2") or  ("turbulence33_s3tsep10bs128lr0.01af3") or 
                    ("turbulence34_s3tsep10bs128lr0.001af1") or ("turbulence35_s3tsep10bs128lr0.001af2") or ("turbulence36_s3tsep10bs128lr0.001af3") or 
                    ("turbulence37_s3tsep10bs128lr0.0001af1") or ("turbulence38_s3tsep10bs128lr0.0001af2") or ("turbulence39_s3tsep10bs128lr0.0001af3") or
                    ("turbulence310_s3tsep10bs256lr0.01af1") or ("turbulence311_s3tsep10bs256lr0.01af2") or ("turbulence312_s3tsep10bs256lr0.01af3") or
                    ("turbulence313_s3tsep10bs256lr0.001af1") or ("turbulence314_s3tsep10bs256lr0.001af2") or ("turbulence315_s3tsep10bs256lr0.001af3") or 
                    ("turbulence316_s3tsep10bs256lr0.0001af1") or ("turbulence317_s3tsep10bs256lr0.0001af2") or ("turbulence318_s3tsep10bs256lr0.0001af3") or
                    ("turbulence319_s3tsep20bs128lr0.01af1") or ("turbulence320_s3tsep20bs128lr0.01af2") or ("turbulence321_s3tsep20bs128lr0.01af3") or 
                    ("turbulence322_s3tsep20bs128lr0.001af1") or ("turbulence323_s3tsep20bs128lr0.001af2") or ("turbulence324_s3tsep20bs128lr0.001af3") or 
                    ("turbulence325_s3tsep20bs128lr0.0001af1") or ("turbulence326_s3tsep20bs128lr0.0001af2") or ("turbulence327_s3tsep20bs128lr0.0001af3") or 
                    ("turbulence328_s3tsep20bs256lr0.01af1") or ("turbulence329_s3tsep20bs256lr0.01af2") or ("turbulence330_s3tsep20bs256lr0.01af3") or 
                    ("turbulence331_s3tsep20bs256lr0.001af1") or ("turbulence332_s3tsep20bs256lr0.001af2") or ("turbulence333_s3tsep20bs256lr0.001af3") or 
                    ("turbulence334_s3tsep20bs256lr0.0001af1") or ("turbulence335_s3tsep20bs256lr0.0001af2") or ("turbulence336_s3tsep20bs256lr0.0001af3") or
                    ("turbulence337_s3tsep40bs128lr0.01af1") or ("turbulence338_s3tsep40bs128lr0.01af2") or ("turbulence339_s3tsep40bs128lr0.01af3") or
                    ("turbulence340_s3tsep40bs128lr0.001af1") or ("turbulence341_s3tsep40bs128lr0.001af2") or ("turbulence342_s3tsep40bs128lr0.001af3") or
                    ("turbulence343_s3tsep40bs128lr0.0001af1") or ("turbulence344_s3tsep40bs128lr0.0001af2") or ("turbulence345_s3tsep40bs128lr0.0001af3") or
                    ("turbulence346_s3tsep40bs256lr0.01af1") or ("turbulence347_s3tsep40bs256lr0.01af2") or ("turbulence348_s3tsep40bs256lr0.01af3") or
                    ("turbulence349_s3tsep40bs256lr0.001af1") or ("turbulence350_s3tsep40bs256lr0.001af2") or ("turbulence351_s3tsep40bs256lr0.001af3") or 
                    ("turbulence352_s3tsep40bs256lr0.0001af1") or ("turbulence353_s3tsep40bs256lr0.0001af2") or ("turbulence354_s3tsep40bs256lr0.0001af3") or
                    ("turbulence355_s3tsep80bs128lr0.01af1") or ("turbulence356_s3tsep80bs128lr0.01af2") or ("turbulence357_s3tsep80bs128lr0.01af3") or
                    ("turbulence358_s3tsep80bs128lr0.001af1") or ("turbulence359_s3tsep80bs128lr0.001af2") or ("turbulence360_s3tsep80bs128lr0.001af3") or
                    ("turbulence361_s3tsep80bs128lr0.0001af1") or ("turbulence362_s3tsep80bs128lr0.0001af2") or  ("turbulence363_s3tsep80bs128lr0.0001af3") or
                    ("turbulence364_s3tsep80bs256lr0.01af1") or ("turbulence365_s3tsep80bs256lr0.01af2") or ("turbulence366_s3tsep80bs256lr0.01af3") or 
                    ("turbulence367_s3tsep80bs256lr0.001af1") or ("turbulence368_s3tsep80bs256lr0.001af2") or ("turbulence369_s3tsep80bs256lr0.001af3") or
                    ("turbulence370_s3tsep80bs256lr0.0001af1") or ("turbulence371_s3tsep80bs256lr0.0001af2") or ("turbulence372_s3tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3") )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "hiddenStatesgru1": data1["hsoutputhiddenstates"],
                "gruweights1": data1["gruweights"],
                "zerohidden1":data1["zerohidden"],
                "hiddenStatesreshape1": data1["hiddenstates"],
                "hiddenstateo1":data1["hiddenstateso"],
                "testinputs1": data1["test_input"],
                "actualValues1": data1["test_output"],
                "predictions1": data1["prediction"],
                "pcaprojection1":data1["pcaprojection"],
                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                "projectiono1": data1["projectiono"],
                "umapprojection1":data1["umapprojection"],

                "c01":data1["c0"],
                "c11":data1["c1"],
                "c21":data1["c2"],

                "co01":data1["co0"],
                "co11":data1["co1"],
                "co21":data1["co2"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })

     #5 ts 10ts
    if( (dataset1==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3") )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],

                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })

     #5 ts 20ts
    if( (dataset1==("turbulence51_s5tsep10bs128lr0.01af1") or ("turbulence52_s5tsep10bs128lr0.01af2") or ("turbulence53_s5tsep10bs128lr0.01af3") or
                ("turbulence54_s5tsep10bs128lr0.001af1") or ("turbulence55_s5tsep10bs128lr0.001af2") or ("turbulence56_s5tsep10bs128lr0.001af3") or
                ("turbulence57_s5tsep10bs128lr0.0001af1") or ("turbulence58_s5tsep10bs128lr0.0001af2") or ("turbulence59_s5tsep10bs128lr0.0001af3") or
                ("turbulence510_s5tsep10bs256lr0.01af1") or ("turbulence511_s5tsep10bs256lr0.01af2") or ("turbulence512_s5tsep10bs256lr0.01af3") or 
                ("turbulence513_s5tsep10bs256lr0.001af1") or ("turbulence514_s5tsep10bs256lr0.001af2") or ("turbulence515_s5tsep10bs256lr0.001af3") or
                ("turbulence516_s5tsep10bs256lr0.0001af1") or ("turbulence517_s5tsep10bs256lr0.0001af2") or ("turbulence518_s5tsep10bs256lr0.0001af3") or
                ("turbulence519_s5tsep20bs128lr0.01af1") or ("turbulence520_s5tsep20bs128lr0.01af2") or ("turbulence521_s5tsep20bs128lr0.01af3") or 
                ("turbulence522_s5tsep20bs128lr0.001af1") or ("turbulence523_s5tsep20bs128lr0.001af2") or ("turbulence524_s5tsep20bs128lr0.001af3") or 
                ("turbulence525_s5tsep20bs128lr0.0001af1") or ("turbulence526_s5tsep20bs128lr0.0001af2") or ("turbulence527_s5tsep20bs128lr0.0001af3") or 
                ("turbulence528_s5tsep20bs256lr0.01af1") or ("turbulence529_s5tsep20bs256lr0.01af2") or ("turbulence530_s5tsep20bs256lr0.01af3") or 
                ("turbulence531_s5tsep20bs256lr0.001af1") or ("turbulence532_s5tsep20bs256lr0.001af2") or ("turbulence533_s5tsep20bs256lr0.001af3") or 
                ("turbulence534_s5tsep20bs256lr0.0001af1") or ("turbulence535_s5tsep20bs256lr0.0001af2") or ("turbulence536_s5tsep20bs256lr0.0001af3")or
                ("turbulence537_s5tsep40bs128lr0.01af1") or ("turbulence538_s5tsep40bs128lr0.01af2") or ("turbulence539_s5tsep40bs128lr0.01af3") or
                ("turbulence540_s5tsep40bs128lr0.001af1") or ("turbulence541_s5tsep40bs128lr0.001af2") or ("turbulence542_s5tsep40bs128lr0.001af3") or 
                ("turbulence543_s5tsep40bs128lr0.0001af1") or ("turbulence544_s5tsep40bs128lr0.0001af2") or ("turbulence545_s5tsep40bs128lr0.0001af3") or
                ("turbulence546_s5tsep40bs256lr0.01af1") or ("turbulence547_s5tsep40bs256lr0.01af2") or ("turbulence548_s5tsep40bs256lr0.01af3") or
                ("turbulence549_s5tsep40bs256lr0.001af1") or ("turbulence550_s5tsep40bs256lr0.001af2") or ("turbulence551_s5tsep40bs256lr0.001af3") or
                ("turbulence552_s5tsep40bs256lr0.0001af1") or ("turbulence553_s5tsep40bs256lr0.0001af2") or ("turbulence554_s5tsep40bs256lr0.0001af3") or 
                ("turbulence555_s5tsep80bs128lr0.01af1") or ("turbulence556_s5tsep80bs128lr0.01af2") or ("turbulence557_s5tsep80bs128lr0.01af3") or
                ("turbulence558_s5tsep80bs128lr0.001af1") or ("turbulence559_s5tsep80bs128lr0.001af2") or ("turbulence560_s5tsep80bs128lr0.001af3") or 
                ("turbulence561_s5tsep80bs128lr0.0001af1") or ("turbulence562_s5tsep80bs128lr0.0001af2") or ("turbulence563_s5tsep80bs128lr0.0001af3") or
                ("turbulence564_s5tsep80bs256lr0.01af1") or ("turbulence565_s5tsep80bs256lr0.01af2") or ("turbulence566_s5tsep80bs256lr0.01af3") or
                ("turbulence567_s5tsep80bs256lr0.001af1") or ("turbulence568_s5tsep80bs256lr0.001af2") or ("turbulence569_s5tsep80bs256lr0.001af3") or
                ("turbulence570_s5tsep80bs256lr0.0001af1") or ("turbulence571_s5tsep80bs256lr0.0001af2") or ("turbulence572_s5tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3")  )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],

                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })

    #10 ts 20ts
    if( (dataset1==("turbulence101_s10tsep10bs128lr001af1") or  ("turbulence102_s10tsep10bs128lr0.01af2") or  ("turbulence103_s10tsep10bs128lr0.01af3")
                 or ("turbulence104_s10tsep10bs128lr0.001af1") or ("turbulence105_s10tsep10bs128lr0.001af2") or ("turbulence106_s10tsep10bs128lr0.001af3")
                 or ("turbulence107_s10tsep10bs128lr0.0001af1") or ("turbulence108_s10tsep10bs128lr0.0001af2") or ("turbulence109_s10tsep10bs128lr0.0001af3")
                 or ("turbulence1010_s10tsep10bs256lr0.01af1") or ("turbulence1011_s10tsep10bs256lr0.01af2") or ("turbulence1012_s10tsep10bs256lr0.01af3")
                 or ("turbulence1013_s10tsep10bs256lr0.001af1") or ("turbulence1014_s10tsep10bs256lr0.001af2") or ("turbulence1015_s10tsep10bs256lr0.001af3")
                 or ("turbulence1016_s10tsep10bs256lr0.0001af1") or ("turbulence1017_s10tsep10bs256lr0.0001af2") or ("turbulence1018_s10tsep10bs256lr0.0001af3")
                 or ("turbulence1019_s10tsep20bs128lr0.01af1") or ("turbulence1020_s10tsep20bs128lr0.01af2") or ("turbulence1021_s10tsep20bs128lr0.01af3")
                 or ("turbulence1022_s10tsep20bs128lr0.001af1") or ("turbulence1023_s10tsep20bs128lr0.001af2") or ("turbulence1024_s10tsep20bs128lr0.001af3")
                 or ("turbulence1025_s10tsep20bs128lr0.0001af1") or ("turbulence1026_s10tsep20bs128lr0.0001af2") or ("turbulence1027_s10tsep20bs128lr0.0001af3")
                 or ("turbulence1028_s10tsep20bs256lr0.01af1") or ("turbulence1029_s10tsep20bs256lr0.01af2") or ("turbulence1030_s10tsep20bs256lr0.01af3")
                 or ("turbulence1031_s10tsep20bs256lr0.001af1") or ("turbulence1032_s10tsep20bs256lr0.001af2") or ("turbulence1033_s10tsep20bs256lr0.001af3")
                 or ("turbulence1034_s10tsep20bs256lr0.0001af1") or ("turbulence1035_s10tsep20bs256lr0.0001af2") or ("turbulence1036_s10tsep20bs256lr0.0001af3")
                 or ("turbulence1037_s10tsep40bs128lr0.01af1") or ("turbulence1038_s10tsep40bs128lr0.01af2") or ("turbulence1039_s10tsep40bs128lr0.01af3")
                 or ("turbulence1040_s10tsep40bs128lr0.001af1") or ("turbulence1041_s10tsep40bs128lr0.001af2") or ("turbulence1042_s10tsep40bs128lr0.001af3")
                 or ("turbulence1043_s10tsep40bs128lr0.0001af1") or ("turbulence1044_s10tsep40bs128lr0.0001af2") or ("turbulence1045_s10tsep40bs128lr0.0001af3")
                 or ("turbulence1046_s10tsep40bs256lr0.01af1") or ("turbulence1047_s10tsep40bs256lr0.01af2") or ("turbulence1048_s10tsep40bs256lr0.01af3")
                 or ("turbulence1049_s10tsep40bs256lr0.001af1") or ("turbulence1050_s10tsep40bs256lr0.001af2") or ("turbulence1051_s10tsep40bs256lr0.001af3")
                 or ("turbulence1052_s10tsep40bs256lr0.0001af1") or ("turbulence1053_s10tsep40bs256lr0.0001af2") or ("turbulence1054_s10tsep40bs256lr0.0001af3")
                 or ("turbulence1055_s10tsep80bs128lr0.01af1") or ("turbulence1056_s10tsep80bs128lr0.01af2") or ("turbulence1057_s10tsep80bs128lr0.01af3")
                 or ("turbulence1058_s10tsep80bs128lr0.001af1") or ("turbulence1059_s10tsep80bs128lr0.001af2") or ("turbulence1060_s10tsep80bs128lr0.001af3")
                 or ("turbulence1061_s10tsep80bs128lr0.0001af1") or ("turbulence1062_s10tsep80bs128lr0.0001af2") or ("turbulence1063_s10tsep80bs128lr0.0001af3")
                 or ("turbulence1064_s10tsep80bs256lr0.01af1") or ("turbulence1065_s10tsep80bs256lr0.01af2") or ("turbulence1066_s10tsep80bs256lr0.01af3")
                 or ("turbulence1067_s10tsep80bs256lr0.001af1") or ("turbulence1068_s10tsep80bs256lr0.001af2") or ("turbulence1069_s10tsep80bs256lr0.001af3")
                 or ("turbulence1070_s10tsep80bs256lr0.0001af1") or ("turbulence1071_s10tsep80bs256lr0.0001af2") or ("turbulence1072_s10tsep80bs256lr0.0001af3") ) and 
        (dataset2==("turbulence201_s20tsep10bs128lr0.01af1") or  ("turbulence202_s20tsep10bs128lr0.01af2") or  ("turbulence203_s20tsep10bs128lr0.01af3") or
                 ("turbulence204_s20tsep10bs128lr0.001af1") or ("turbulence205_s20tsep10bs128lr0.001af2") or ("turbulence206_s20tsep10bs128lr0.001af3") or 
                 ("turbulence207_s20tsep10bs128lr0.0001af1") or ("turbulence208_s20tsep10bs128lr0.0001af2") or ("turbulence209_s20tsep10bs128lr0.0001af3") or 
                 ("turbulence2010_s20tsep10bs256lr0.01af1") or ("turbulence2011_s20tsep10bs256lr0.01af2") or ("turbulence2012_s20tsep10bs256lr0.01af3") or 
                 ("turbulence2013_s20tsep10bs256lr0.001af1") or ("turbulence2014_s20tsep10bs256lr0.001af2") or ("turbulence2015_s20tsep10bs256lr0.001af3") or 
                 ("turbulence2016_s20tsep10bs256lr0.0001af1") or ("turbulence2017_s20tsep10bs256lr0.0001af2") or ("turbulence2018_s20tsep10bs256lr0.0001af3") or 
                 ("turbulence2019_s20tsep20bs128lr0.01af1") or ("turbulence2020_s20tsep20bs128lr0.01af2") or ("turbulence2021_s20tsep20bs128lr0.01af3") or
                 ("turbulence2022_s20tsep20bs128lr0.001af1") or ("turbulence2023_s20tsep20bs128lr0.001af2") or ("turbulence2024_s20tsep20bs128lr0.001af3") or 
                 ("turbulence2025_s20tsep20bs128lr0.0001af1") or ("turbulence2026_s20tsep20bs128lr0.0001af2") or ("turbulence2027_s20tsep20bs128lr0.0001af3") or
                 ("turbulence2028_s20tsep20bs256lr0.01af1") or ("turbulence2029_s20tsep20bs256lr0.01af2") or ("turbulence2030_s20tsep20bs256lr0.01af3") or 
                 ("turbulence2031_s20tsep20bs256lr0.001af1") or ("turbulence2032_s20tsep20bs256lr0.001af2") or ("turbulence2033_s20tsep20bs256lr0.001af3") or 
                 ("turbulence2034_s20tsep20bs256lr0.0001af1") or ("turbulence2035_s20tsep20bs256lr0.0001af2") or ("turbulence2036_s20tsep20bs256lr0.0001af3") or
                 ("turbulence2037_s20tsep40bs128lr0.01af1") or ("turbulence2038_s20tsep40bs128lr0.01af2") or ("turbulence2039_s20tsep40bs128lr0.01af3") or
                 ("turbulence2040_s20tsep40bs128lr0.001af1") or ("turbulence2041_s20tsep40bs128lr0.001af2") or ("turbulence2042_s20tsep40bs128lr0.001af3") or
                 ("turbulence2043_s20tsep40bs128lr0.0001af1") or ("turbulence2044_s20tsep40bs128lr0.0001af2") or ("turbulence2045_s20tsep40bs128lr0.0001af3") or
                 ("turbulence2046_s20tsep40bs256lr0.01af1") or ("turbulence2047_s20tsep40bs256lr0.01af2") or ("turbulence2048_s20tsep40bs256lr0.01af3") or 
                 ("turbulence2049_s20tsep40bs256lr0.001af1") or ("turbulence2050_s20tsep40bs256lr0.001af2") or ("turbulence2051_s20tsep40bs256lr0.001af3") or
                 ("turbulence2052_s20tsep40bs256lr0.0001af1") or ("turbulence2053_s20tsep40bs256lr0.0001af2") or ("turbulence2054_s20tsep40bs256lr0.0001af3") or
                 ("turbulence2055_s20tsep80bs128lr0.01af1") or ("turbulence2056_s20tsep80bs128lr0.01af2") or ("turbulence2057_s20tsep80bs128lr0.01af3") or
                 ("turbulence2058_s20tsep80bs128lr0.001af1") or ("turbulence2059_s20tsep80bs128lr0.001af2") or ("turbulence2060_s20tsep80bs128lr0.001af3") or
                 ("turbulence2061_s20tsep80bs128lr0.0001af1") or ("turbulence2062_s20tsep80bs128lr0.0001af2") or ("turbulence2063_s20tsep80bs128lr0.0001af3") or
                 ("turbulence2064_s20tsep80bs256lr0.01af1") or ("turbulence2065_s20tsep80bs256lr0.01af2") or ("turbulence2066_s20tsep80bs256lr0.01af3") or
                 ("turbulence2067_s20tsep80bs256lr0.001af1") or ("turbulence2068_s20tsep80bs256lr0.001af2") or ("turbulence2069_s20tsep80bs256lr0.001af3") or
                 ("turbulence2070_s20tsep80bs256lr0.0001af1") or ("turbulence2071_s20tsep80bs256lr0.0001af2") or ("turbulence2072_s20tsep80bs256lr0.0001af3")  )):
    # read json file
        with open(userData[dataset1]) as f:
            data1 = json.load(f)
        with open(userData[dataset2]) as f:
            data2 = json.load(f)
            
        return jsonify({
                
                
                "seqlength1":data1["seqlength"],
                "time_increment1":data1["time_increment"],
                "accuracy1": data1["model_accuracy"],
                "testinputs1": data1["test_input"],

                "projection1": data1["projection"],
                "nfeatures1": data1["nfeatures"],
                                
                "seqlength2":data2["seqlength"],
                "time_increment2":data2["time_increment"],
                "accuracy2": data2["model_accuracy"],
                "testinputs2": data2["test_input"],
                "projection2": data2["projection"],
                "nfeatures2": data2["nfeatures"],
                
                })

@app.route('/zerohidden')
def zero():
    global userData
    cwd = os.getcwd()
    print(cwd)

    userData = toml.load("/home/satish/thesis/flask/repos/MA-Aanand-Turbulence/visualization/userData.toml")

    return render_template('zerohidden.html',datasets=userData.keys())

@app.route('/overall')
def overallcomparison():

    return render_template('parallelplot.html')

@app.route("/errortable")
def table():
  
 
  with open("/home/satish/thesis/flask/repos/MA-Aanand-Turbulence/visualization/parallel4.csv") as file:
    return render_template("RMSE.html", csv=file)

if __name__ == '__main__':
   app.run(host='127.0.0.1',port='5000',debug=True)




