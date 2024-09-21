from tictactoe import minimax
X = "X"
O = "O"
EMPTY = "EMPTY"

board = [[EMPTY, O, X],
        [O, O, X],
        [EMPTY, EMPTY, EMPTY]]

print(minimax(board))