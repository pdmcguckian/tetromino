# Tetromino Algorithm

## The Challenge
Presented with a target pattern of tetrominoes, attempt to find a tiling solution - balancing the accuracy of the result and the time taken. For example:

![Example](/Images/Example.png)

The target is provided in the form of a list of lists. Where there is a 1, a piece should be placed. The solution should give each point as a tuple - (0,0) for empty space or (pieceCount, pieceType) where a piece was placed.

## My Solution
My solution creates a neighbours grid scoring each space needing filled based on the number of neighbours also requiring filling. Then, starting at points with only one neighbour, it uses greedy iterative depth first search to place tiles - selecting steps based on which has the lowest number of nieghbours until an entire tile is placed. After a piece is placed it updates the surrounding spaces in the neighbours grid to keep the greedy logic accurate. This process is is then repeated for all points needing filled until its unable to place any more tiles.

## The Results
My solution scored among the highest in the year - striking a good balance of speed an accuracy. Accuracies were high for all grid densities and the algorithm scalled well for large grid sizes.

![Result](/Images/Results.png)
