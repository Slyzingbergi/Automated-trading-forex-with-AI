# Problem Statement
Because forex trading is more risky than investing in other forms, but returns are also very high.  
To reduce the risk, I thought the AI knowledge can fix this problem.  
I know that other investors have their own trading techniques and in this project I use basic techniques to help me train model.  
The goal of this system is to reduce risk and get profit by Automated trading.  

# Hypotheses
I noticed that often when the needle is happened then Trigger of the graph will be reverse.   
I call it a needle, but I don't know what other people call it.
I called the candle like this 3 picture below are needle.  
![01](https://user-images.githubusercontent.com/28421585/48298019-298e9580-e4f9-11e8-8b50-38746ff51a2f.JPG)
![02](https://user-images.githubusercontent.com/28421585/48298020-2dbab300-e4f9-11e8-9148-c51820e60f71.JPG)
![03](https://user-images.githubusercontent.com/28421585/48298021-30b5a380-e4f9-11e8-9c42-2ee9dbcf6de7.JPG)  
 I will create the feature that indicates the candle is a needle to train my model.  



# Data Exploration and Visualization  
This data is only 7 columns.("date","time","open","high","low","close","volume")  
Initially, I had to clean up the data since the information has been available since 1971.  
It's too far from the present and volume and price is too different from now.  
I need to use data that is as close to the current as possible, so I picked up data starting from 2014.  
The value of Volume is high, so I divide it by 100 to reduce the distribution of data.  
Plot the graph of volume and time.  
1. Volume versus Time  
![vol_time](https://user-images.githubusercontent.com/28421585/48298231-1ed5ff80-e4fd-11e8-826f-f91067ed13ea.JPG)  
2. Avg.Volume versus Time  
![avgvol_time](https://user-images.githubusercontent.com/28421585/48298244-68bee580-e4fd-11e8-9046-b184ccd5cb64.JPG)  
From figure 1,2 It is noted that the volume is high in time 12:00, 16:00, 18:00  
3. Avg.Change versus Time  
![change_time](https://user-images.githubusercontent.com/28421585/48298410-3498f400-e500-11e8-937b-13217b776f6b.JPG)  
I used the data "change" to confirm Figure 1,2 that it affects the price.  
I will explain "change" data in the Feature Transformation and Engineering topic.
I think it can loop through the Data Exploration Visualization process and Feature Transformation Engineering process.  

# Feature Transformation and Engineering  
I will describe each of the features that I am taking from this step.  
1."time" I transform time value to 2 class, 0 is mean  low volume time and 1 is high volume time.(Refer from Figure 1,2)  
  
2."change" This feature come from different of open price and close price.  
  
3."move" This feature come from different of high price and low price.  
  
4."pre_high" is high price value of 4 hours previous.  
  
5."pre_low" is low price value of 4 hours previous.  
  
6."pre_move" is "move" value of 4 hours previous.  
  
7."pre_change" is "change" value of 4 hours previous.  
  
8."needle" This feature come from different of move and change.
  
9."percent_needle" This feature come from percent of change/move.  
  
10."chk_move" This feature for check needle are happen. I make this feature from "move" value have to more than 0.150 and "percent needle" value lower than 25%, 1 is happened and 0 is not happened.  
  
# Model Building


# Business Applications and Implementation


# Results and Key Learnings

