# Tetromino Algorithm

## The Challenge
Presented with a target pattern of tetrominoes, attempt to find a tiling solution - balancing between accuracy of the result and the time taken. For example:

The target is provided in the form of a list of lists. Where there is a 1, a piece should be placed. The solution should give each point as a tuple - (0,0) for empty space or (pieceCount, pieceType) where a piece was placed. For example:

## My Solution
My solution scores each space needing filled based on the number of neighbours also requiring filling. Then, starting at points with only one neighbour, it uses greedy iterative depth first search to place tiles - selecting steps based on which has the lowest number of nieghbours until an entire tile is placed. After a piece is placed it updates the surrounding spaces in the neighbours grid to keep the greedy logic accurate. This process is is then repeated for all points needing filled until its unable to place any more tiles.