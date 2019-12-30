"""
Math 590
Project 3
Fall 2019

Partner 1: Feng Hu (fh65)
Partner 2: Lingzhuo Zhao (lz171)
Date: Nov/11/2019
"""

# Import math and p3tests.
from p3tests import *
from p3currencies import *
from arr2mat import *

################################################################################

"""
detectArbitrage
This function detects negative cost cycles from a graph
Input: Currencies object for the exchange rates, and a tolerance value.
Output: A list of vertex ranks corresponding to the negative cost cycle
"""


def detectArbitrage(currencies, tol=1e-15):
    # Set initial dist and prev
    for vertex in currencies.adjList:
        vertex.dist = math.inf
        vertex.prev = None
    # Choose adjList[0] as our start vertex
    currencies.adjList[0].dist = 0

    # Iterate |v|-1 times
    for it in range(0, len(currencies.adjList) - 1):
        # Look at each vertex
        for u in currencies.adjList:
            # Check each neighbor and update prediction & prev
            for neighbor in u.neigh:
                # Update distance if the new value is better
                if neighbor.dist > u.dist + currencies.adjMat[u.rank][neighbor.rank] + tol:
                    neighbor.dist = u.dist + \
                        currencies.adjMat[u.rank][neighbor.rank]
                    neighbor.prev = u

    # Initialize empty list for negative cost cycle
    neg_cyc = []

    # Run Bellman-Ford one more time to detect neg_cyc
    neg_v_list = detectArbitrage_helper(currencies, tol)
    neg_cyc_list = []

    # Return empty list if no negative cycles exist
    if not neg_v_list:
        return neg_cyc

    # Trace back to add ranks to the list otherwise
    else:
        for neg_v in neg_v_list:
            # Assign current to start tracing back
            curr = currencies.adjList[neg_v]

            # Push new rank values to the front of list
            # if the new rank is not repeated in the list
            while curr.rank not in neg_cyc:
                neg_cyc.insert(0, curr.rank)
                curr = curr.prev

            # Put in the starting vertex's rank again
            index = neg_cyc.index(curr.rank)
            neg_cyc.insert(0, curr.rank)

            # Slice the list to get negative cycle
            neg_cyc_list.append(neg_cyc[0:index + 2])

    # a dict to store info.
    max_neg_cyc = {}
    max_neg_cyc['v_list'] = []
    max_neg_cyc['arb'] = 1

    for neg_c_ind in range(0, len(neg_cyc_list)):
        neg_c = neg_cyc_list[neg_c_ind]
        arb = 1
        for cInd in range(0, len(neg_c) - 1):
            arb *= currencies.rates[neg_c[cInd]][neg_c[cInd + 1]]
        # Update max_neg_cyc.
        if arb > max_neg_cyc['arb']:
            max_neg_cyc['v_list'] = neg_c
            max_neg_cyc['arb'] = arb

    return max_neg_cyc['v_list']


"""
detectArbitrage_helper
This function runs Bellman-Ford one more time to detect negative cycle
Input: Currencies object for the exchange rates, and a tolerance value.
Output: A rank value if there is negative cost cycle (None if there isn't)
"""


def detectArbitrage_helper(currencies, tol=1e-15):
    changeList = []

    # Look at each vertex
    for u in currencies.adjList:
        # Check each neighbor and update prediction & prev
        for neighbor in u.neigh:
            # Update if the new value is better
            if neighbor.dist > u.dist + currencies.adjMat[u.rank][neighbor.rank] + tol:
                neighbor.prev = u
                # Return the rank value of the neighbor changed
                changeList.append(neighbor.rank)
    # Return none if no arbitrage is found
    return changeList


################################################################################

"""
rates2mat
This functions obtains an adjacency matrix from exchange rate matrix
Input: A matrix with all exchange rates
Output: An adjacency matrix with log value edge weights
"""


def rates2mat(rates):
    # Previously: this only returns a copy of the rates matrix.
    # Currently: use log values as edge weights
    return [[-math.log10(R) for R in row] for row in rates]


"""
Main function.
"""
if __name__ == "__main__":
    testRates()
