import urllib.request
import csv
import json
from pymongo import MongoClient
from datetime import datetime
from xml.dom.minidom import parse
from collections import OrderedDict

# sudo mongod --dbpath /usr/local/var/mongodb
client = MongoClient('localhost', 27017)  # Make a connection
db = client['currency']  # DB: currency
db_prices = db['prices']  # Collection: prices

codes = ['USD', 'JPY', 'BGN', 'CYP', 'CZK', 'DKK', 'EEK', 'GBP', 'HUF', 'LTL', 'LVL', 'MTL', 'PLN', 'ROL', 'RON', 'SEK', 'SIT', 'SKK',
         'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRL', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR',
         'NZD', 'PHP', 'SGD', 'THB', 'ZAR']
codes7 = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'SGD', 'CHF', 'MYR', 'JPY']


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


def checkToday():
    # Read from the xml, get today's currency.
    u1 = urllib.request.urlopen(
        'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
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
    if not db_prices.find({"date": date}).count():
        insert1Day(rates, cur, date=date)


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
    checkToday()
