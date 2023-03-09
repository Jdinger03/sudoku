import random

def generate_puzzle():
    puzzle = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            puzzle[i][j] = (i*3 + i//3 + j) % 9 + 1
    random.shuffle(puzzle)
    for i in range(9):
        random.shuffle(puzzle[i])
    return puzzle

def remove_numbers(puzzle, num_remove):
    puzzle_copy = [row[:] for row in puzzle]
    num_removed = 0
    while num_removed < num_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle_copy[row][col] != 0:
            puzzle_copy[row][col] = 0
            num_removed += 1
    return puzzle_copy

puzzle = generate_puzzle()
puzzle = remove_numbers(puzzle, 30)

for row in puzzle:
    print(row)
