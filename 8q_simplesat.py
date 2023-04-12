# Define the size of the board
n = 8

# Define the list of variables
variables = [ [i * n + j + 1 for j in range(n)] for i in range(n)]

# Define the list of clauses
clauses = []

# Add a clause for each row
for i in range(n):
    clauses.append(variables[i])

# Add a clause for each column
for j in range(n):
    clauses.append([variables[i][j] for i in range(n)])

# Add a clause for each diagonal from left to right
for k in range(-n+1, n):
    clause = []
    for i in range(n):
        j = i - k
        if j >= 0 and j < n:
            clause.append(variables[i][j])
    if len(clause) > 0:
        clauses.append(clause)

# Add a clause for each diagonal from right to left
for k in range(0, 2*n-1):
    clause = []
    for i in range(n):
        j = k - i
        if j >= 0 and j < n:
            clause.append(variables[i][j])
    if len(clause) > 0:
        clauses.append(clause)

# Define a function to convert the variable index to row and column
def get_position(variable):
    return ((variable - 1) // n, (variable - 1) % n)

# Define a function to print the solution
def print_solution(solution):
    for i in range(n):
        row = ""
        for j in range(n):
            if solution[variables[i][j]]:
                row += "Q "
            else:
                row += ". "
        print(row)

# Define a function to solve the problem
def solve():
    # Import the subprocess module
    import subprocess
    
    # Define the path to the SAT solver
    solver_path = "minisat"

    # Write the SAT problem to a file
    with open("problem.cnf", "w") as f:
        f.write("p cnf {} {}\n".format(n*n, len(clauses)))
        for clause in clauses:
            f.write(" ".join([str(x) for x in clause]) + " 0\n")

    # Call the SAT solver
    output = subprocess.check_output([solver_path, "problem.cnf"]).decode().split("\n")
    if output[0] == "SAT":
        solution = [False] * (n*n+1)
        for variable in output[1].split(" ")[:-1]:
            value = int(variable)
            if value > 0:
                solution[value] = True
        print_solution(solution)
    else:
        print("No solution found")

# Solve the problem
solve()

