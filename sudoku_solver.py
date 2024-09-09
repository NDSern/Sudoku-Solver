class SudokuSolver:
    def solveSudoku(self, board: list[list[str]]) -> None:
        def isValid(row, col, val):
            for i in range(9):
                # Check for row and col
                if board[row][i] == val or board[i][col] == val:
                    return False
                
                # Check the 3x3 square
                grid_row = 3 * (row // 3) + i // 3
                grid_col = 3 * (col // 3) + i % 3
                if board[grid_row][grid_col] == val:
                    return False
            return True


        def dfs(row, col):
            if row > 8:
                return True
            
            if col > 8:
                return dfs(row+1, 0)

            if board[row][col] != '.':
                return dfs(row, col+1)

            for i in range(1, 10):
                if isValid(row, col, str(i)):
                    board[row][col] = str(i)
                    if dfs(row, col+1):
                        return True
                    board[row][col] = '.'
                
            return False
    
        if dfs(0, 0):
            return True
        else:
            return False