# -*- coding: utf-8 -*-
"""
Date: 2022/03/04
Author: Giray Balci
"""

import pandas as pd
import matplotlib.pyplot as plt
import time
import os


#directory check for img folder
script_dir = os.path.dirname(__file__)
file_dir = os.path.join(script_dir, 'img/')

if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
    
prefix = "2point_"
    
csv_file_name = prefix + "data_out.csv"




#%%

#read spice measurement file
measFile_name = "data/Calibration.txt"

with open(measFile_name, 'r') as f:
    lines = f.readlines()
    
f.close()


numOfMeas = 0
isStartOfMeas = False
counter = -1 #mark measurement row as -1

measList = list()

df = pd.DataFrame()

for line in lines:

    #get the number of runs
    if(line.startswith(".step ")):
        numOfRuns = int(line.split('=')[1])
    
    #get the number of measurements and name of measurement
    if(line.startswith("Measurement: ")):
        nameOfMeas = line.split(': ')[1][:-1]
        
        #mark the start of a new measurement
        isStartOfMeas = True
   
    if(isStartOfMeas):
        if((counter > 1) and (counter <= numOfRuns)):
            value = line.split()[1]

            measList.append(value)
        
        counter += 1

        #append to dataframe and reset counter
        if(counter > numOfRuns):   
            df_meas = (pd.DataFrame({nameOfMeas:measList}))
            result = pd.concat([df, df_meas], axis=1)
            
            df = result
            
            counter = -1
            isStartOfMeas = False 
            measList.clear()
        
        
print("Number of measurements: ", numOfMeas)
print("Number of runs: ", numOfRuns)


#store data into a csv file 
#if you want to append data to existing file make below variable True
#LTspice sometimes crashes. To append new data to previous data,
#isAppend can be used


isAppend = False

if(isAppend):
    data = pd.read_csv(csv_file_name)
    
    cols_existing = data.columns
    cols_append = df.columns
    
    #check if datas hold
    if(cols_existing.all() == cols_append.all()):

        data = data.append(df, ignore_index=True)
        data.to_csv(csv_file_name, index=False)
        
        print("Data appended")
        print("Now, number of data entries: ", len(data))

else:
    df.to_csv(csv_file_name, index=False)


#%% read data and plot the histograms
data = pd.read_csv(csv_file_name)

my_dpi = 200

fig, axs = plt.subplots(figsize=(10,5))
plt.rc('axes', axisbelow=True) #put grid behind

column_names = data.columns

for col in column_names:
    fig.clf() #clear figure for each iteration

    data[col].plot.hist(bins=50)
     
    plt.title("Histogram of "+ str.capitalize(col))
    plt.xlabel(str.capitalize(col), fontsize=14)    
    plt.grid(visible=True, which='both', linestyle='--')

    file_name = prefix + "histogram_" + col + ".png"
    
    fig.savefig(file_dir + file_name , dpi=my_dpi, format="png")

    time.sleep(0.05)     #wait between file writes. 50 ms
    

#%% box plots
file_name = prefix + "boxplot.png"

fig.clf()
fig = plt.gcf()

i = 1
for col in column_names:
    plt.tight_layout()
    plt.subplot(2,2,i)
    
    data[col].plot.box()
  
    plt.grid(visible=True, which='both', linestyle='--')
    
    i += 1


fig.savefig(file_dir + file_name , dpi=my_dpi)
