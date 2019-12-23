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
                    neighbor.dist = u.dist + currencies.adjMat[u.rank][neighbor.rank]
                    neighbor.prev = u

    # Initialize empty list for negative cost cycle
    neg_cyc = []

    # Run Bellman-Ford one more time to detect neg_cyc
    neg_v = detectArbitrage_helper(currencies, tol)

    # Return empty list if no negative cycles exist
    if neg_v is None:
        return neg_cyc

    # Trace back to add ranks to the list otherwise
    else:
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
        return neg_cyc[0:index + 2]

"""
detectArbitrage_helper
This function runs Bellman-Ford one more time to detect negative cycle
Input: Currencies object for the exchange rates, and a tolerance value.
Output: A rank value if there is negative cost cycle (None if there isn't)
"""


def detectArbitrage_helper(currencies, tol=1e-15):
    # Look at each vertex
    for u in currencies.adjList:
        # Check each neighbor and update prediction & prev
        for neighbor in u.neigh:
            # Update if the new value is better
            if neighbor.dist > u.dist + currencies.adjMat[u.rank][neighbor.rank] + tol:
                neighbor.prev = u
                # Return the rank value of the neighbor changed
                return neighbor.rank
    # Return none if no arbitrage is found
    return None


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
    # testRates()
    arr = [[1, 2, 5],
           [1, 2, 5],
           [1, 2, 5]]
    mat = arr2mat(arr)
    for row in mat:
        print(row)