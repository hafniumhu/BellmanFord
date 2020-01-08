# Import the Currencies class.
from p3currencies import *

"""
testRates function will test all of the exchange rate examples.
"""


def testRates():
    print()
    print('Testing Exchange Rates:')
    c = Currencies()
    # print(c)
    if not c.arbitrage():
        print('No arbitrage for Exchange Rates 0')
    else:
        print('Correct result for Exchange Rates 0')
    print('------------------------')
    return

################################################################################
