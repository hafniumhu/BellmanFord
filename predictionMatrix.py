import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from fbprophet import Prophet

"""
This function inputs datafram with first column ds(Date),
second column historical currency rate.
It returns a array which is the prediction of currency
for next 7 future days. 
"""
def prediction(df):
    #Eliminate empty values
    df = df[np.isfinite(df['y'])]
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=7)
    future.tail()
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    temp = np.array(forecast['yhat'][-7:])
    # fig1 = m.plot(forecast)
    # fig2 = m.plot_components(forecast)
    # plt.show()
    return temp

"""
This function read historical data from cvs file.
Return the 7*10 matrix with prediction currency rates.
"""
def getData(filename):
    df = pd.read_csv(filename)
    df = df[['Currency code', 'Date', 'Units per USD']]
    #Get Date data from the datafram and eliminate repeated date
    date = df['Date']
    date = date.drop_duplicates()
    date = date.dropna()
    date = date.reset_index(drop=True)

    #Get currency exchange rates and eliminate nan data
    allRates = np.array(df['Units per USD'])
    allRates = allRates[np.logical_not(np.isnan(allRates))]
    allRates = allRates.tolist()

    #Initialize historical data to matrix for prediction
    #We need more data to do prediction.
    #Number of rows is number of days we used to predict
    #Each column represents each currency
    matrix = np.zeros((7, 10))
    for i in range(7):
        for k in range(10):
            matrix[i][k] = allRates.pop(0)

    #Concat historical matrix to original datafram
    df = pd.concat([df, pd.DataFrame(matrix)], axis=1)

    #Initialize prediction matrix
    Predictionmatrix = np.zeros((7, 10))

    #call predicton function for each currency
    for k in range(10):
        a = pd.concat([date, df[k]], axis=1)
        a = a.rename(columns={"Date": "ds", k: "y"})
        predictionData = prediction(a)
        for m in range(7):
            Predictionmatrix[m][k] = predictionData[m]


    return Predictionmatrix

if __name__ == '__main__':
    file = "currencies12081214.csv"
    Predictionmatrix = getData(file)
    print(Predictionmatrix)