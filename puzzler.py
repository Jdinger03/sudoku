import random

def generate_sudoku():
    # Initialize a blank 9x9 Sudoku grid
    grid = [[0 for i in range(9)] for j in range(9)]
    
    # Generate a valid Sudoku solution using backtracking algorithm
    solve_sudoku(grid)
    
    # Remove random cells to create an unfinished Sudoku puzzle
    for i in range(40): # adjust the number of cells to remove here
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0
    
    return grid

def solve_sudoku(grid):
    # Find an empty cell to fill
    row, col = find_empty_cell(grid)
    
    # If no empty cell is found, the grid is solved
    if row == -1 and col == -1:
        return True
    
    # Try all possible values for the empty cell
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            # Recursively solve the remaining Sudoku grid
            if solve_sudoku(grid):
                return True
            
            # If the solution is not found, backtrack and try the next value
            grid[row][col] = 0
            
    # If none of the values work, the Sudoku puzzle is unsolvable
    return False

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

def is_valid_move(grid, row, col, num):
    # Check if num is already in the same row, column or 3x3 square
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    square_row = (row // 3) * 3
    square_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[square_row+i][square_col+j] == num:
                return False
    return True

# Generate and print the unfinished Sudoku puzzle
puzzle = generate_sudoku()
for row in puzzle:
    print(row)
