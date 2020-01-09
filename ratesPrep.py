import urllib.request
import csv
import json
from pymongo import MongoClient
from datetime import datetime
from xml.dom.minidom import parse
from predictionMatrix import currency_codes
import configparser


codes = ['USD', 'JPY', 'BGN', 'CYP', 'CZK', 'DKK', 'EEK', 'GBP', 'HUF', 'LTL', 'LVL', 'MTL', 'PLN', 'ROL', 'RON', 'SEK', 'SIT', 'SKK',
         'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRL', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR',
         'NZD', 'PHP', 'SGD', 'THB', 'ZAR']

# Currency codes used in Bellman-ford.
codes7 = currency_codes


def baseUSD(source, target):
    if(source == 'N/A' or target == 'N/A'):
        return 0
    my = float(target) / float(source)
    return float("{0:.4f}".format(my))


def insert1Day(row, currency_codes, date):
    list = []
    i = 0
    for code in currency_codes:
        if code in codes7:
            list.append(dict({'Date': datetime.strptime(date, '%Y-%m-%d'),
                              'Currency code': code,
                              'Units per USD': baseUSD(row[0], row[i])}))
        i += 1
    list.append(dict({'Date': datetime.strptime(date, '%Y-%m-%d'),
                      'Currency code': 'EUR',
                      'Units per USD': baseUSD(row[0], 1)}))
    db_prices.insert_many(list)


def updateToday(url):
    # Read from the xml, get today's currency.
    u1 = urllib.request.urlopen(url)
    dom = parse(u1)
    itemlist = dom.getElementsByTagName('Cube')
    cur = []
    rates = []
    for s in itemlist:
        try:
            cur.append(str(s.attributes['currency'].value))
            rates.append(float(s.attributes['rate'].value))
        except:
            try:
                rates.remove(float(s.attributes['currency'].value))
            except:
                pass
    for s in itemlist:
        try:
            date = (str(s.attributes['time'].value))
        except:
            pass
    # If not included in db, insert today's currency data.
    if not db_prices.find({"Date": datetime.strptime(date, '%Y-%m-%d')}).count():
        insert1Day(rates, cur, date=date)


def historic_data():
    with open('eurofxref-hist.csv', 'r') as csvfile:
        db_prices.delete_many({})
        # Read historic currencies.
        csvFile = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(csvFile)
        for row in csvFile:
            date = row[0]
            # Insert not included data.
            del row[0]
            insert1Day(row, codes, date=date)


if __name__ == '__main__':

    """ Generate config file.
    config = configparser.ConfigParser()
    config['atlas'] = {'url': 'mongodb://Yueying:11223344@cluster0-shard-00-00-x0eas.mongodb.net:27017,cluster0-shard-00-01-x0eas.mongodb.net:27017,cluster0-shard-00-02-x0eas.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&w=majority',
                       'db_name': 'bf',
                       'collection_name': 'prices'}
    config['ECB_ref'] = {
        'daily': 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    """

    # Make a connection
    config = configparser.ConfigParser()
    config.read('config.ini')
    client = MongoClient(config['atlas']['url'])
    db = client[config['atlas']['db_name']]
    db_prices = db[config['atlas']['collection_name']]  # Collection: prices
    # db_prices.delete_many(
    #     {'Date': {"$gt": datetime(2020, 1, 7)}})
    updateToday(config['ECB_ref']['daily'])
