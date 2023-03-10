import random
import numpy as np
from datetime import datetime
from pytz import timezone
from PIL import Image, ImageDraw, ImageFont

def generate_sudoku(difficulty):
    # Initialize a blank 9x9 Sudoku grid
    grid = [[0 for i in range(9)] for j in range(9)]

    # Generate a valid Sudoku solution using backtracking algorithm
    solve_sudoku(grid)

    # Remove random cells to create an unfinished Sudoku puzzle
    if difficulty == 'easy':
        num_cells_to_remove = 45
    elif difficulty == 'medium':
        num_cells_to_remove = 51
    elif difficulty == 'hard':
        num_cells_to_remove = 57
    else:
        print('Invalid difficulty level. Generating puzzle with medium difficulty.')
        num_cells_to_remove = 51

    for i in range(num_cells_to_remove):
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

# Generate and save the Sudoku puzzle as an image file
def save_sudoku_image(grid, filename):
    # Create a blank image
    img = Image.new("RGB", (450, 450), color="white")

    # Draw the grid lines
    draw = ImageDraw.Draw(img)
    for i in range(10):
        if i % 3 == 0:
            # Bold line for each 3x3 section
            draw.line([(50*i, 0), (50*i, 450)], width=3, fill="black")
            draw.line([(0, 50*i), (450, 50*i)], width=3, fill="black")
        else:
            draw.line([(50*i, 0), (50*i, 450)], fill="black")
            draw.line([(0, 50*i), (450, 50*i)], fill="black")

    # Draw the numbers on the image
    font = ImageFont.truetype("arial.ttf", 40)
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                num = str(grid[row][col])
                w, h = draw.textsize(num, font=font)
                x = col*50 + (50 - w) / 2
                y = row*50 + (50 - h) / 2
                draw.text((x, y), num, fill="black", font=font)

    # Format the filename with difficulty level and date and time
    filename = f"Sudoku {difficulty.capitalize()} {datetime.now(timezone('Australia/Sydney')).strftime('%d-%m-%Y %H-%M-%S')}.png"

    # Save the image file
    img.save(filename)

    return filename

# Generate a Sudoku puzzle and save it as an image file
difficulty = input("Enter difficulty level (easy/medium/hard): ")
grid = generate_sudoku(difficulty)
filename = "sudoku.png"
directory = r"C:\Users\jackr\OneDrive\Desktop\Games\Sudoku"
save_sudoku_image(grid, filename)
print(f"Sudoku puzzle saved as {filename} in the {directory} directory")
