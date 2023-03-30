class EightQueens:
    def __init__(self):
        self.board = [0] * 8

    def is_valid(self, col, row):
        for i in range(col):
            if self.board[i] == row or \
               self.board[i] - i == row - col or \
               self.board[i] + i == row + col:
                return False
        return True

    def solve(self, col):
        if col == 8:
            return True
        for row in range(8):
            if self.is_valid(col, row):
                self.board[col] = row
                if self.solve(col + 1):
                    return True
        return False

    def print_solution(self):
        for row in range(8):
            line = ""
            for col in range(8):
                if self.board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)

solver = EightQueens()
if solver.solve(0):
    solver.print_solution()
else:
    print("No solution found.")
