"""
arr2mat

"""
import math


"""
Input: 7 arrays containing exchange rates based on USD
Output: a matrix of exchange rates
"""
def arr2mat(arr):
    # Initialize rate to infinity
    day = len(arr)
    curr = len(arr[0])
    size = day * curr
    rates = [[math.inf for x in range(size)] for x in range(size)]

    # Construct rates
    for i in range(size):
        # Fill out by row
        curr_remainder = i % day
        curr_start = i - curr_remainder

        # Get backward entries
        if curr_remainder == day - 1:
            rates[i][curr_start] = 1

        # Above diagonal entries
        for j in range(curr_start + day + i % day, size, day):
            rates[i][j] = arr[i % day][j // day] / arr[i % day][i//day]

        for j in range(size):
            # Same currency entries (1's)
            if i <= j < curr_start + day:
                rates[i][j] = 1

            # Below diagonal entries
            if j < i:
                if rates[i][j] != 1 and rates[i][j] != math.inf:
                    rates[i][j] = 1 / rates[j][i]

    return rates
