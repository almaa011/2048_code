from Helper import *
import numpy as np
import time 

# Returns the expected utility for the current state.
def Decision(grid, max=True):
    limit = 4
    start = time.perf_counter()

    if max:
        return Maximize(grid=grid, depth=limit, start=start)
    else:
        return Expectation(grid=grid, depth=limit, start=start)
        
# For the maximizing player (the one making moves)
def Maximize(grid, depth, start):
    if terminal(grid) or depth == 0 or (time.perf_counter() - start) > 0.04:
        return Eval(grid)

    maxUtility = -np.inf
    for child in children(grid):
        maxUtility = max(maxUtility, Expectation(grid=child, depth=depth-1, start=start))
        
    return maxUtility

# For the chance node: calculating the expected utility from random tile placements.
def Expectation(grid, depth, start):
    if terminal(grid) or depth == 0 or (time.perf_counter() - start) > 0.04:

        return Eval(grid)

    empty = grid.getAvailableCells()
    if not empty:
        return Eval(grid)

    expectedUtility = 0.0
    # The probability is divided equally among empty cells.
    p_cell = 1.0 / len(empty)
    for pos in empty:
        grid2 = grid.clone()
        grid4 = grid.clone()

        grid2.insertTile(pos, 2)
        grid4.insertTile(pos, 4)

        # Weigh the outcomes: 0.9 for tile 2, 0.1 for tile 4.
        utility2 = Maximize(grid2, depth-1, start)
        utility4 = Maximize(grid4, depth-1, start)
        expectedUtility += p_cell * (0.9 * utility2 + 0.1 * utility4)

    return expectedUtility
