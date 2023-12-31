class Grid:

    # Create a new grid
    def __init__(self, rows, cols):
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    # Indexing operations
    def __getitem__(self, coords):
        (row, col) = coords
        return self.grid[row][col]

    def __setitem__(self, coords, val):
        (row, col) = coords
        self.grid[row][col] = val
