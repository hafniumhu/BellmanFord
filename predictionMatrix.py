import contextlib
import sys
import os
import pandas as pd
import numpy as np
from pymongo import MongoClient, DESCENDING
from matplotlib import pyplot as plt
from fbprophet import Prophet
import datetime
import csv
import logging
from suppress_stdout_stderr import suppress_stdout_stderr
logging.getLogger('fbprophet').setLevel(logging.WARNING)


"""
This function inputs datafram with first column ds(Date),
second column historical currency rate.
It returns a array which is the prediction of currency
for next 7 future days. 
"""

currency_codes = ['USD', 'EUR', 'GBP', 'INR',
                  'AUD', 'CAD', 'SGD', 'CHF', 'MYR', 'JPY']

with contextlib.redirect_stdout(None):
    def prediction(df):
        # Eliminate empty values
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


def getData(fileName):
    df = pd.read_csv(fileName)
    df = df[['Currency code', 'Date', 'Units per USD']]
    # Get Date data from the datafram and eliminate repeated date
    date = df['Date']
    date = date.drop_duplicates()
    date = date.dropna()
    date = date.reset_index(drop=True)

    # Get currency exchange rates and eliminate nan data
    allRates = np.array(df['Units per USD'])
    allRates = allRates[np.logical_not(np.isnan(allRates))]
    allRates = allRates.tolist()

    # Initialize historical data to matrix for prediction
    # We need more data to do prediction.
    # Number of rows is number of days we used to predict
    # Each column represents each currency
    matrix = np.zeros((7, 10))
    for i in range(7):
        for k in range(10):
            matrix[i][k] = allRates.pop(0)

    # Concat historical matrix to original datafram
    df = pd.concat([df, pd.DataFrame(matrix)], axis=1)

    # Initialize prediction matrix
    Predictionmatrix = np.zeros((7, 10))

    # call predicton function for each currency
    for k in range(10):
        a = pd.concat([date, df[k]], axis=1)
        a = a.rename(columns={"Date": "ds", k: "y"})
        with suppress_stdout_stderr():
            predictionData = prediction(a)
        for m in range(7):
            Predictionmatrix[m][k] = predictionData[m]

    return Predictionmatrix


"""
db2csv(fileName):
generate csv file using db query result.
"""


def db2csv(fileName):
    # db preparation.
    client = MongoClient('localhost', 27017)  # Client: Make a connection
    db = client['currency']  # DB: currency
    db_prices = db['prices']  # Collection: prices

    # query: date & 10 currencies.
    df = db_prices.find({
        'Date': {'$lt': datetime.datetime.now(),
                 '$gte': datetime.datetime.now() - datetime.timedelta(days=60),
                 }, 'Currency code': {'$in': currency_codes}}).sort('Date', DESCENDING)
    # write a new csv file.
    with open(fileName, 'w', encoding='utf-8', newline='') as files:
        csvfiles = csv.DictWriter(
            files, fieldnames=['Currency code', 'Date', 'Units per USD'])
        csvfiles.writeheader()
        n = 1
        for i in df:
            csvfiles.writerow(
                {'Currency code': i['Currency code'],
                 'Date': i['Date'],
                 'Units per USD': i['Units per USD']})
            n += 1
    # close db connection.
    client.close()


"""
curr_codes_date():
Generate rates matrix header.
"""


def curr_codes_date():
    curr_codes_withdate = []
    for code in currency_codes:
        # Todo: change number postfix into date.
        for k in range(7):
            curr_codes_withdate.append(code + str(k))
    return curr_codes_withdate


"""
predict():
return the raw rates matrix: 7 * 10.
"""


def predict():
    fileName = "data.csv"
    # generate csv file contain recent 60 days rates.
    db2csv(fileName)
    # predict next 7 days.
    print("Predicting...")
    Predictionmatrix = getData(fileName)
    return Predictionmatrix


# if __name__ == '__main__':
#     print(predict())
