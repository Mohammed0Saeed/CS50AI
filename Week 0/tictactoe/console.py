from tictactoe import *
import os

#os.system('cls' if os.name == 'nt' else 'clear')

X = "X"
O = "O"
EMPTY = None

board = initial_state()

while True:
    # import the board after committing changes
    print_board(board)

    # take a move from X
    move = input("Enter a move in form of 'i j': ")
    move = move.split(" ")
    move = (int(move[0]), int(move[1]))

    # apply the move to the board
    board = result(board, move)
    print_board(board)

    # wait for AI response
    move = minimax(board)
    board = result(board, move)
    print_board(board)

    # stop if there is a winner
    if terminal(board):
        print(winner(board), "wins")
        break


minimax(board)
