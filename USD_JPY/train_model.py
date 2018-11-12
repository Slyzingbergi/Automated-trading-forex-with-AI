# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:28:49 2018

@author: watsapon
"""
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from sklearn.metrics import mean_squared_error


def run_train():
    df = pd.read_csv('USDJPY240_1.csv')
    df = df[31286:] ##34640
    time = df['time']
    time = time.tolist()
    time = [ 1 if x in ['8:00', '12:00', '16:00'] else 0 for x in time ]
    df['time'] = time
    df = df.drop(columns=['date'])
    df['volume'] = df['volume']/100
    #df = df.drop(columns=['volume'])
    #day = str(day)
    
    change = df.close - df.open
    df['change'] = change
    move = df.high - df.low
    df['move'] = move
    df3 = df[1:].reset_index()
    df2 = df[:-1].reset_index()
    df2 = df2.drop(columns=['index'])
    df3 = df3.drop(columns=['index'])
    pre_high = df2['high']
    pre_low =  df2['low']
    pre_move = df2['move']
    pre_change = df2['change']
    df3['pre_high'] = pre_high
    df3['pre_low'] = pre_low
    df3['pre_move'] = pre_move
    df3['pre_change'] = pre_change
    
    
    df3['needle'] = df3.move - abs(df3.change)
    df3['percent_needle'] = (abs(df3.change)/df3.move)*100
    df3 = df3.dropna()
    chk_move = df3['move'].tolist()
    needle_point = [1 if x > 0.150 else 0 for x in chk_move]
    percent = df3['percent_needle'].tolist()
    
    for i in range(len(percent)):
        if percent[i] < 25 and needle_point[i] == 1 :
            needle_point[i] = 1
        else:
            needle_point[i] = 0
    
    df3['chk_move'] = needle_point
    
    df3 = df3.sort_index(axis=1)
    train = df3
    test = df3.sample(frac=0.10, replace=True)
    train = train.reset_index()
    train = train.drop(columns=['index'])
    test = test.reset_index()
    test = test.drop(columns=['index'])
    train_input = train[:-1]
        
    train_output = train[1:]
    train_output = train_output[['close']]
      
    test_input = test[:-1]  
    test_output =test[1:]
    test_output = test_output[['close']]
    
    model = Sequential()
    model.add(Dense(12, input_dim=15, activation='relu'))
    ###model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='rmsprop')
    model.fit(train_input, train_output, epochs=1500, verbose=1)
    
    predict_new = model.predict(test_input)
    er =  mean_squared_error(test_output, predict_new)  
    
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    
    model.save_weights("model.h5")
    print("Saved model to disk")
    return(er)
 
    
er = 100
while er > 0.05 :
    er = run_train()
#    if  :
#        break
