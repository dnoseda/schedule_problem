# First, import the required libraries
from pysat.solvers import Glucose3
from pysat.formula import CNF

# Define the size of the chessboard (8x8 for the 8 Queens problem)
board_size = 8

# Initialize an empty list to store the clauses
clauses = []

# Define a helper function to convert (row, col) coordinates to a variable number
def var_num(row, col):
    return row * board_size + col + 1

# Add the first set of constraints: each row must contain exactly one queen
for row in range(board_size):
    clause = [var_num(row, col) for col in range(board_size)]
    clauses.append(clause)
    for i in range(board_size):
        for j in range(i + 1, board_size):
            # Add a clause to ensure that two queens cannot be in the same row
            clauses.append([-var_num(row, i), -var_num(row, j)])

# Add the second set of constraints: each column must contain exactly one queen
for col in range(board_size):
    clause = [var_num(row, col) for row in range(board_size)]
    clauses.append(clause)
    for i in range(board_size):
        for j in range(i + 1, board_size):
            # Add a clause to ensure that two queens cannot be in the same column
            clauses.append([-var_num(i, col), -var_num(j, col)])

# Add the third set of constraints: no two queens can be on the same diagonal
for i in range(board_size):
    for j in range(board_size):
        if i != j:
            # Add a clause to ensure that two queens cannot be on the same diagonal
            clauses.append([-var_num(i, j), -var_num(j, i)])

# Create a CNF formula from the list of clauses
cnf = CNF()
cnf.extend(clauses)

# Use the Glucose3 SAT solver to check if the formula is satisfiable
with Glucose3(bootstrap_with=cnf) as solver:
    # If the formula is satisfiable, print the solution
    if solver.solve():
        model = solver.get_model()
        for row in range(board_size):
            line = ""
            for col in range(board_size):
                # If the variable is true, there is a queen on that square
                if var_num(row, col) in model:
                    line += "Q "
                else:
                    line += ". "
            print(line)
    else:
        print("No solution found")

