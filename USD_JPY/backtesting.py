# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 16:44:47 2018

@author: watsapon
"""
################################## important #############################################
################## This model("model3.json") are only working on USD_JPY #################
############### if need to use other instruments have to train new AI model ##############
##########################################################################################
import pandas as pd # for prepocess before predict
from keras.models import model_from_json # for load AI model
from oandapyV20 import API # for get token
from oandapyV20.exceptions import V20Error # for can't connect to oanda server
import oandapyV20.endpoints.instruments as instruments # for get candles
import matplotlib.pyplot as plt # for plot graph

access_token = "d5b008dfd3a08c3c6c45a24b44d4070d-86bd33acf53c2da478adfbc9d6b45bd9" # my token from oanda 
client = API(access_token=access_token) # set token
lor = [] # for sent request to oanda sever
params = { "count":5000, "granularity": "H4" }  # set 5000 candles is max , H4 per 1 candles

lor.append(instruments.InstrumentsCandles(instrument="USD_JPY", params=params))  # set syntex of USD_JPY for request to sever

sss = 700    # equity
trade = []  # 
side = []  #  for close order
cur = ""
lot = 150  # size of lot  150 == 0.15 in standard account
space = 3 # space is cost when open order
cross_day = 1.5 # cross_day is cost when hold order cross a day
x = [] # x-axis graph is candles
y = [] # y-axis graph is equity
############################################

json_file = open("model6.json", 'r') # open model 
loaded_model_json = json_file.read() # read model 
json_file.close() # close
loaded_model = model_from_json(loaded_model_json) # tranform to keras 
loaded_model.load_weights("model6.h5") # load weights file
print("Loaded model from disk")
############################################
#json_file = open("model4.json", 'r') # open model 
#loaded_model_json = json_file.read() # read model 
#json_file.close() # close
#loaded_model2 = model_from_json(loaded_model_json) # tranform to keras 
#loaded_model2.load_weights("model4.h5") # load weights file
############################################
for r in lor:
    try:
        rv = client.request(r)  # sent request and get dictionary data
        candles = rv.get('candles') # get only candles data form dictionary type
        for i in range(len(candles)): # run every candles
#            if sss > 1400 :
            lot = (sss/4700) * 1000
            space = lot/50
            cross_day = lot/100
            if (candles[i].get('complete')): # check status of candles 
#############################################################################################################
################## data preprocessing to predict START ######################################################
#############################################################################################################
                vol = int(candles[i].get('volume'))/100  # volume of current candles divide 100
                mid = candles[i].get('mid') # mid is dictionary type , have open ,high, low , close data in this
                o = float(mid.get('o'))  #get open price data of current
                h = float(mid.get('h'))  #get high price data of current
                l = float(mid.get('l'))  #get low price data of current
                c = float(mid.get('c'))  #get close price data of current
                time = (candles[i].get('time'))[11:16]  # get only hour and minutes
                if time in ['8:00', '12:00', '16:00']:
                    time = 1 # give day time to be 1
                else:
                    time = 0 # give night time to be 0
                change = c - o # get diffent cost from open to close
                change = float("%.3f" % change)  # set type to float
                move = h - l # get diffent cost from high to low
                move = float("%.3f" % move)  #set type to float
                needle = move - abs(change) # get needle thing
                if move == 0 : #  debug
                    percent_needle = 100
                else:
                    percent_needle = (abs(change)/move)*100  #calculate percent of needle
                needle_point = 1 if move > 0.150 and percent_needle < 25 else 0  # if this condition be needle
                old = candles[i-1].get('mid') # get previous candles
                pre_h = float(old.get('h')) # get previous high
                pre_l = float(old.get('l')) # get previous low
                pre_o = float(old.get('o'))  # get previous open
                pre_c = float(old.get('c')) # get previous close
                pre_move = pre_h - pre_l  # get previous move
                pre_change = pre_c - pre_o  # get previous change
                test_input = {'time': [time],'open': [o], 'high': [h],'low':[l],'close':[c],'volume': [vol],'change':[change],
                              'move':[move],'pre_high': [pre_h],'pre_low':[pre_l], 'pre_move': [pre_move],'pre_change':[pre_change],
                              'needle':[needle],'percent_needle':[percent_needle],'chk_move':[needle_point] 
                              } # all data to dictionary type
################################################################################################################
################## data preprocessing to predict END ###########################################################
################################################################################################################
                test_input = pd.DataFrame(test_input) # change input data type to dataframe for predict
                test_input = test_input.sort_index(axis=1) # sort colums
                predict_val = loaded_model.predict(test_input) # predicted data
                predict_val = float("%.3f" % predict_val) # predicted data to float type

                real_close = float((candles[i+1].get('mid')).get('c'))  # real close data of next candles for check backtesting
                next_l = float((candles[i+1].get('mid')).get('l'))  # low cost data of next candles for check backtesting when equity over on lowest
                next_h = float((candles[i+1].get('mid')).get('h'))  # high cost data of next candles for check backtesting when equity over on highest
                next_o = float((candles[i+1].get('mid')).get('o'))  # this is open cost of current order
                if i % 7 == 0 and trade != []:   # if hold order cross a day minus this value
                    sss = sss - cross_day
                dif = predict_val - next_o  # this is different value of predict value and open cost

                if  dif < -0.125 and trade == [] :#and dif2 < -0.100 : #-0.125 # open sell order if different value lower -0.125
                    print("sell")
                    trade.append(next_o)  # open order
                    cur = "sell"  # save status
                    side.append(True) 
                elif  dif > 0.125 and trade == [] :#and dif2 > 0.100: # 0.125 # open buy order if different value more than 0.125
                    print("buy")
                    trade.append(next_o) # open order
                    cur = "buy"  # save status
                    side.append(True)
                elif trade != [] : # if hold order
                    if cur == "buy" : # if hold buy order
                        if sss + (next_l - trade[0])*lot < 0 : # fail when equity lower 0 
                            print("fail low" + str(sss + (next_l - trade[0])*lot)) # fail
                            break
                        elif real_close > next_o : # hold order when candle still right way
                            print("True")
                            side.append(True) # get history for check 
                        else: # if candle are wrong way
                            side.append(False) # get history for check 
                            if len(side)> 1:
                                if side[i] == False and side[i-1] == False: # close order when have double wrong way candle
                                    order = trade.pop() # get position of trade order
                                    cur = ""
                                    print((real_close - order)*lot - space) # calculate summary of this order
                                    sss = sss + (real_close - order)*lot - space # calculate equity
                                    print(sss) # print summary

                    elif cur == "sell" : # if hold sell order
                        if sss + (trade[0] - next_h)*lot < 0 : # fail when equity lower 0 
                            print("fail low" + str(sss + (trade[0] - next_h)*lot)) # fail
                            break
                        elif real_close < next_o : # hold order when candle still right way
                            print("True")
                            side.append(True) # get history for check 
                        else: # if candle are wrong way
                            side.append(False) # get history for check 
                            if len(side)> 1:
                                if side[i] == False and side[i-1] == False: # close order when have double wrong way candle
                                    order = trade.pop()  # get position of trade order
                                    cur = ""
                                    print((order - real_close)*lot - space) # calculate summary of this order
                                    sss = sss + (order - real_close)*lot -space # calculate equity
                                    print(sss) # print summary

                else : # if predict value different lower 0.125 then skip wait next candle
                    print("skip")
                    side.append("skip")  # get history for check 
            x.append(i)  # get history for plot graph
            y.append(sss)   # get history for plot graph

        print("True=" + str(side.count(True)) + "   False=" + str(side.count(False)) , "  skip= " + str(side.count("skip"))) # print all action
    except V20Error as e:
        print("OOPS: {:d} {:s}".format(e.code, e.msg)) # error when can't connect to server oadan
        
plt.plot(x, y) # plot graph
plt.xlabel('4hr_candles', color='C0')  # label X
plt.ylabel('USD', color='C0') # label Y
plt.show() # show graph