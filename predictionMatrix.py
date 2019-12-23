import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from fbprophet import Prophet


def prediction(df):
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

def getData():
    df = pd.read_csv('currencies12081214.csv')
    df = df[['Currency code', 'Date', 'Units per USD']]
    date = df['Date']
    date = date.drop_duplicates()
    date = date.dropna()
    date = date.reset_index(drop=True)


    allRates = np.array(df['Units per USD'])
    allRates = allRates[np.logical_not(np.isnan(allRates))]
    allRates = allRates.tolist()

    matrix = np.zeros((7, 10))
    for i in range(7):
        for k in range(10):
            matrix[i][k] = allRates.pop(0)

    df = pd.concat([df, pd.DataFrame(matrix)], axis=1)
    #for i in range(10):
     #   df = df.rename(columns={i: df['Currency code'][i]})

    Predictionmatrix = np.zeros((7, 10))

    for i in range(7):
        for k in range(10):
            matrix[i][k] = allRates.pop(0)
    for k in range(10):
        a = pd.concat([date, df[k]], axis=1)
        predictionData = prediction(a)
        predictionmatrix[]


    return Predictionmatrix