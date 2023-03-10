import random
import numpy as np
from datetime import datetime
from pytz import timezone
from PIL import Image, ImageDraw, ImageFont
import pathlib
import copy

def generate_sudoku(difficulty):
    top_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(top_row)

    grid = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        grid[0][i] = top_row[i]

    num_cells_to_remove = get_num_cells_to_remove(difficulty)

    while True:
        puzzle = copy.deepcopy(grid)
        remove_cells(puzzle, num_cells_to_remove)
        num_solutions = solve_sudoku(puzzle, count=True)
        if num_solutions == 1:
            break

    return puzzle

def get_num_cells_to_remove(difficulty):
    if difficulty == 'super easy':
        num_cells_to_remove = 30
    elif difficulty == 'easy':
        num_cells_to_remove = 40
    elif difficulty == 'medium':
        num_cells_to_remove = 45
    elif difficulty == 'hard':
        num_cells_to_remove = 50
    elif difficulty == 'expert':
        num_cells_to_remove = 60
    else:
        print('Invalid difficulty level. Generating puzzle with medium difficulty.')
        num_cells_to_remove = 45

    return num_cells_to_remove

def remove_cells(grid, num_cells_to_remove):
    for i in range(num_cells_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0

def solve_sudoku(grid, count=False):
    row, col = find_empty_cell(grid)

    if row == -1 and col == -1:
        return 1

    num_solutions = 0
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num

            if count:
                num_solutions += solve_sudoku(grid, count=True)
                if num_solutions > 1:
                    return num_solutions
            else:
                if solve_sudoku(grid):
                    return True
            grid[row][col] = 0

    if count:
        return num_solutions
    else:
        return False

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

def is_valid_move(grid, row, col, num):
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

def save_sudoku_image(grid, filename):
    img = Image.new("RGB", (450, 450), color="white")

    draw = ImageDraw.Draw(img)
    for i in range(10):
        if i % 3 == 0:
            draw.line([(50*i, 0), (50*i, 450)], width=3, fill="black")
            draw.line([(0, 50*i), (450, 50*i)], width=3, fill="black")
        else:
            draw.line([(50*i, 0), (50*i, 450)], fill="black")
            draw.line([(0, 50*i), (450, 50*i)], fill="black")

    font = ImageFont.truetype("arial.ttf", 40)
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                num = str(grid[row][col])
                w, h = draw.textsize(num, font=font)
                x = col*50 + (50 - w) / 2
                y = row*50 + (50 - h) / 2
                draw.text((x, y), num, fill="black", font=font)

    filename = f"Sudoku {difficulty.capitalize()} {datetime.now(timezone('Australia/Sydney')).strftime('%d-%m-%Y %H-%M-%S')}.png"

    # Save the image file
    img.save(filename)

    return filename

difficulty = input("Enter difficulty level (super easy/easy/medium/hard/expert): ")
grid = generate_sudoku(difficulty)
filename = f"Sudoku {difficulty.capitalize()} {datetime.now(timezone('Australia/Sydney')).strftime('%d-%m-%Y %H-%M-%S')}.png"
directory = pathlib.Path().absolute()
save_sudoku_image(grid, filename)
print(f"Sudoku puzzle saved as {filename} in the {directory} directory")
