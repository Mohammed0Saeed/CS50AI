"""
Tic Tac Toe Player

The application user interface was made by the course, i did only wrote the functions in this files
I also made a terminal visualization of the game in console.py 
"""

import math, copy, os

X = "X"
O = "O"
EMPTY = None

def print_board(board):
    """
    Prints a new game board with the latest move
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        for cell in row:
            print(f"|{cell}|", end="")
        print("\n--------------------")

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # intialize two variables to count how much Xs and Os are there in the board
    counter_x = 0
    counter_o = 0

    # checking each box in the board
    # if the box is x or o increase its counter
    for row in board:
        for box in row:
            if box == "X":
                counter_x += 1
            elif box == "O":
                counter_o += 1

    # if X is more than O, return O
    if counter_x > counter_o:
        return O
    # else if O more than X or the board is empty return X
    elif counter_o > counter_x or (counter_o == 0 and counter_x == 0):
        return X
    if counter_x == counter_o:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # an array that includes all the possible boxes
    available_actions = set()

    for i in range(3):
        for j in range(3):
            # if the box is empty, append its location to the available actions
            if board[i][j] not in ["X","O"]:
                available_actions.add((i,j))

    return available_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # create a modifiable copy of the original board
    newBoard = copy.deepcopy(board)

    # input the action to the new board
    if action in actions(board):
        newBoard[int(action[0])][int(action[1])] = player(board)
    else:
        raise ValueError("invalid action")

    # return the new board
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # an array with all the possible winning setuations
    possible_cases = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    # iterate through the possible solution, and if X or O wins return the winner
    for case in possible_cases:
        if case == ["X", "X", "X"]:
            return X
        elif case == ["O", "O", "O"]:
            return O

    # if none is winner return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if there is a winner
    if winner(board) != None:
        return True

    # check if all the cells are full and there is no possible move
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # if the board is full return True
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # check if the game is over
    if terminal(board) == True:
        # check if the winner is X
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1

    # return 0 if no one won or the game is still on hold
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game ended return None
    if terminal(board):
        return None
    # detect whether X or O has to play
    # if the player is X, then use the max function
    if player(board) == X:
        # a dictionary to include each move with its optimal points
        possible_solutions = {}
        # iterate through all the possible moves for X in an array
        for action in actions(board):
            # get the new board from the possible moves of X
            new_board = result(board, action)
            if utility(new_board) == 1:
                return action
            # an array to gather the utility values of the possibles boards
            points = []
            # check if there are some actions yet
            if len(actions(new_board)) != 0:
                # iterate through each possible move for O
                for act in actions(new_board):
                    points.append(utility(result(new_board, act)))
            else:
                # add the values of the current boards
                points.append(utility(new_board))
            # get the lowest point among the points
            possible_solutions[action] = min(points)
        possible_solutions = sorted(possible_solutions.items(), key=lambda item: item[1])
        return possible_solutions[-1][0]
    
    elif player(board) == O:
        # a dictionary to include each move with its optimal points
        possible_solutions = {}
        # iterate through all the possible moves for O in an array
        for action in actions(board):
            # get the new board from the possible moves of O
            new_board = result(board, action)
            # check if this action a winning move
            if utility(new_board) == -1:
                return action
            # an array to gather the utility values of the possibles boards
            points = []
            # check if there are some actions yet
            if len(actions(new_board)) != 0:
                # an array to gather the utility values of the possibles moves of X
                # iterate through each possible move for X
                for act in actions(new_board):
                    points.append(utility(result(new_board, act)))
            else:
                # add the values of the current boards
                points.append(utility(new_board))
            # get the lowest point among the points
            possible_solutions[action] = max(points)
        possible_solutions = sorted(possible_solutions.items(), key=lambda item: item[1])
        return possible_solutions[0][0]
