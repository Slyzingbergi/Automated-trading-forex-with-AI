# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:48:44 2018

@author: watsapon
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('USDJPY240_1.csv')
df = df[31286:]
df = df.reset_index()
df['change'] = abs(df.close - df.open)
df['volume'] = df['volume']/100
df['move'] = df.high - df.low
df['percent_needle'] = (abs(df.change)/df.move)*100
#df = df.dropna()
df['needle'] = df.move - abs(df.change)

needle_point = [1 if x > 0.125 else 0 for x in df['move'].tolist()]
percent = df['percent_needle'].tolist()

for i in range(len(percent)):
    if percent[i] < 25 and needle_point[i] == 1 :
        needle_point[i] = 1
    else:
        needle_point[i] = 0

df['chk_move'] = needle_point



df2 = df[['time','volume']]
df2 = df2.sort_values(['time'])
#df2 = df2.groupby(['time'])['volume'].mean()


plt.scatter(df2['time'], df2['volume']) # plot graph
plt.xlabel('TIME')  # label X
plt.ylabel('VOLUME') # label Y
plt.show() # show graph

#print(df2['time'].value_counts())

df2 = df2.groupby(['time'])['volume'].mean()
df2 = df2.reset_index()

x = np.arange(len(df2['time']))
plt.bar(x, height= df2['volume'])
plt.xticks(x, df2['time']);
plt.xlabel('TIME')  # label X
plt.ylabel('VOLUME') # label Y
plt.show()



df3 = df.groupby(['time'])['change'].mean()
df3 = df3.reset_index()

x = np.arange(len(df3['time']))
plt.bar(x, height= df3['change'])
plt.xticks(x, df3['time'])
plt.xlabel('TIME')  # label X
plt.ylabel('MOVE_VALUE') # label Y
plt.show()



df4 = df.loc[df['chk_move'] == 1]
indexd_df4 = df4.index.values
indexd_df4 = [x+1 for x in indexd_df4 ]
#print(indexd_df4)
df5 = df.iloc[indexd_df4]
#
print(df5.change.mean())

#df5 = df4.loc[df4['change'] >= 0.100]



