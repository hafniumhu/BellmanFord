import pandas as pd
import numpy as np

#read file, set first row as index name
df = pd.read_csv('currencies12081214.csv',index_col=[0])

    #print(df.head(10))

#get all rate in that column
allRates = np.array(df['Units per USD'])
    #print(allRates)

#eliminate nan
allRates= allRates[np.logical_not(np.isnan(allRates))]
    #print(allRates)

#generate and initialize matrix
matrix = np.zeros((7,10))
for i in range(7):
    for k in range(10):
        matrix[i][k] = allRates[i+k]

##test
print(matrix)
print(' ')
print(matrix[0])