"""
Math 590
Project 3
Fall 2019

p3currencies.py
"""

# Import the Vertex class and project3.py functions.
from p3vertex import *
from project3 import detectArbitrage, rates2mat
from arr2mat import *
from predictionMatrix import *

"""
Currencies Class
"""


class Currencies:
    """
    Class attributes:

    rates   # A 2D list of the different exchange rates.
    currs   # A list of the currency names as strings.
    adjList # The adjacency list for the currencies.
    adjMat  # The adjacency matrix for the graph.
    negCyc  # List of vertex ranks in the (potential) negative cost cycle.
    """

    """
    __init__ function to initialize the Currencies.
    """

    def __init__(self):
        # Get the exchange rates and currency names.
        self.rates, self.currs = getRates()

        # Create the adjacency list.
        self.adjList = [Vertex(r) for r in range(0, len(self.currs))]

        # Loop through the adjacency list and set each vertex's neigh list.
        # Note that each currency can be exchanged for any other currency,
        # so the neigh list will be every other vertex.
        for vInd in range(0, len(self.adjList)):
            (self.adjList[vInd]).neigh = self.adjList[0:vInd] + \
                self.adjList[vInd + 1:]

        # Now get the adjacency matrix using the exchange rates.
        # Note: you will write this function above.
        self.adjMat = rates2mat(self.rates)

        # Set the negative cost cycle (nothing yet).
        self.negCyc = []
        return

    """
    __repr__ function to print the Currencies.
    """

    def __repr__(self):
        for cInd in range(0, len(self.currs)):
            print('Rates for %s:' % self.currs[cInd])
            print(self.rates[cInd])
        return ''

    """
    printList function for cleanly printing the adjaceny list.
    Note: skips vertices with no neighbors.
    """

    def printList(self):
        for vertex in self.adjList:
            if len(vertex.neigh) > 0:
                print('Rank: %d' % vertex.rank)
                print('Neighbors:')
                print(vertex.neigh)
                print('')
        return

    """
    printMat function for cleanly printing the adjaceny matrix.
    Note: for the larger matrices, this will still likely be hard to read.
    """

    def printMat(self):
        for row in self.adjMat:
            print(row)
        return

    """
    printArb function prints out the currencies in the negative cycle in order.
    """

    def printArb(self):
        for ind in self.negCyc:
            print(self.currs[ind])
        print()
        return

    """
    arbitrage
    """

    def arbitrage(self):
        # First, use your detectArbitrage function to find a potential
        # negative cost cycle in the graph.
        self.negCyc = detectArbitrage(self)

        # Report if no cycle.
        if len(self.negCyc) == 0:
            print('No Cycle Detected')
            print()
            return False
        else:
            # If there was a cycle reported, check to make sure it was a cycle.
            if len(self.negCyc) < 2:
                raise Exception('Invalid cycle: only 1 vertex')
            elif self.negCyc[0] != self.negCyc[-1]:
                raise Exception('Invalid cycle: start != end')
            else:
                # There was a cycle, check to ensure arbitrage.
                arb = 1
                for cInd in range(0, len(self.negCyc) - 1):
                    arb *= self.rates[self.negCyc[cInd]][self.negCyc[cInd + 1]]
                if arb <= 1:
                    self.printArb()
                    print(arb)
                    raise Exception('No arbitrage in reported cycle!')
                else:
                    print('Arbitrage Cycle:')
                    print()
                    self.printArb()
                    print('For gain of: %f %ss' %
                          ((arb - 1), self.currs[self.negCyc[0]]))
                    print()
                    return True


################################################################################

"""
getRates function will provide the 2D array representing the exchange rates to
the Currencies class's __init__ function.

INPUTS
exchangeNum: which set of rates to select

OUTPUTS
rates: a 2D list representing the exchange rates
currs: the list of currency names
"""

# Print rates formatted matrix.


def format(list):
    formatted = []
    for item in list:
        if(item < 1e-08):
            formatted.append("    ")
        else:
            formatted.append("{:4.2f}".format(item))
    return formatted


def getRates():
    # Get the exchange rates.
    # arr = getData()
    # arr = [[1, 2, 5],
    #        [1, 3, 2],
    #        [1, 9, 5]]

    # Get rates matrix(7 days 10 currencies)
    # by calling predict() in predictionMatrix.py.
    arr = predict()
    # Convert raw rates into rates matrix(based on algorithm design)
    rates = arr2mat(arr)

    # for debug reason(formatted print), convert it into numpy matrix.
    rates = np.array(rates)
    # Print rates matrix
    print('------------------------')
    print('Matrix of exchange rates:')
    print(rates)
    # for row in rates:
    #     print("[{}]".format(', '.join(format(row))))
    print('------------------------')

    # Initialize rates matrix header
    # by calling curr_codes_date() in predictionMatrix.py.
    currs = curr_codes_date()
    # currs = ['USD0', 'USD1', 'USD2',
    #          'GBP0', 'GBP1', 'GBP2',
    #          'INR0', 'INR1', 'INR2']

    # currs = [['USD0', 'GBP0', 'INR0', 'AUD0', 'CAD0', 'SGD0', 'CHF0', 'MYR0', 'JPY0'],
    #          ['USD1', 'GBP1', 'INR1', 'AUD1', 'CAD1', 'SGD1', 'CHF1', 'MYR1', 'JPY1'],
    #          ['USD2', 'GBP2', 'INR2', 'AUD2', 'CAD2', 'SGD2', 'CHF2', 'MYR2', 'JPY2'],
    #          ['USD3', 'GBP3', 'INR3', 'AUD3', 'CAD3', 'SGD3', 'CHF3', 'MYR3', 'JPY3'],
    #          ['USD4', 'GBP4', 'INR4', 'AUD4', 'CAD4', 'SGD4', 'CHF4', 'MYR4', 'JPY4'],
    #          ['USD5', 'GBP5', 'INR5', 'AUD5', 'CAD5', 'SGD5', 'CHF5', 'MYR5', 'JPY5'],
    #          ['USD6', 'GBP6', 'INR6', 'AUD6', 'CAD6', 'SGD6', 'CHF6', 'MYR6', 'JPY6']]

    return rates, currs
