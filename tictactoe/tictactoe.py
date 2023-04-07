"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


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
    # In the initial game state, X gets the first move
    if board == initial_state():
        return X
    
     # Any return value is acceptable if a terminal board is provided as input
    if terminal(board):
        return "Game Over."

    # Count xs and ys to know who's turn is
    moves = count_turns(board)

    # return next player
    return X if moves[X] == moves[O] else O
       
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return "Game Over. No more actions allowed."
    
    possible_actions = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                possible_actions.add((row, column))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # if it is not a valid action, raise an exception
    if board[i][j] != EMPTY:
        raise IndexError('Invalid Action')

    # get a deep copy of the board
    new_state = copy.deepcopy(board)

    # get current player
    pl = player(board)

    # carry action for player
    new_state[i][j] = pl

    # return new_state
    return new_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    main_diag = []
    sec_diag = []
    vertical = []
    horizontal = []

    # check 
    for row in range(len(board[0])):
        for column in range(len(board[0])):
            if row == column:
                main_diag.append(board[row][column])
            
            if ((row + column) == (len(board[0]) - 1)):
                sec_diag.append(board[row][column])
            
            horizontal.append(board[row][column])
            vertical.append(board[column][row])

        # check if all row elements are equal
        if check_all(horizontal):
            return horizontal[0]
        else:
            horizontal = []

        # check if all column elements are equal
        if check_all(vertical):
            return vertical[0]
        else:
            vertical = []

    if check_all(main_diag):
        return main_diag[0]
    
    if check_all(sec_diag):
        return sec_diag[0]
    
    return "No winner"


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game over if there is a winner
    if winner(board) in [X, O]:
        return True

    # Game over if there is no winner
    flat_board = [pl for row in board for pl in row]

    if winner(board) == 'No winner' and EMPTY not in flat_board:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # get player
    pl = player(board)
    
    # get actions
    possible_actions = actions(board)

    # X is the max player
    if pl == X:
  
        # track actions in a stack
        tested_actions = []
        values = []
        for action in possible_actions:
            v = min_value(result(board, action))
            tested_actions.append(action)
            values.append(v)

        return tested_actions[values.index(max(values))]

    
    # O is the min player
    if pl == O:

        # track actions in a stack
        tested_actions = []
        values = []
        for action in possible_actions:
            v = max_value(result(board, action))
            tested_actions.append(action)
            values.append(v)
        
        return tested_actions[values.index(min(values))]
    
def max_value(board):
    """
    Returns the maximum value produced by the min player (min_value function)
    """
    # If in terminal state, return the state utility
    if terminal(board):
        return utility(board)
    
    # set value to be the smallest possible
    v = -math.inf

    # search for the max value by testing possible actions 
    # based on the moves of the min player
    for action in actions(board):
         v = max(v, min_value(result(board, action)))

    return v

def min_value(board):
    """
    Returns the min value produced by the max player (min_value function)
    """
    # If in terminal state, return the state utility
    # If in terminal state, return the state utility
    if terminal(board):
        return utility(board)
    
    # set value to be the largest possible
    v = math.inf

    # search for the max value by testing possible actions 
    # based on the moves of the min player
    for action in actions(board):
         v = min(v, max_value(result(board, action)))

    return v

def count_turns(board):
    """
    Returns dictionary with the number of turns for each player
    """
    turns = {X:0, O:0} 

    for row in board:
        for spot in row:
            if spot == X:
                turns[X] += 1
            elif spot == O:
                turns[O] += 1

    return turns

def check_all(row):
    # check if all row elements are equal
    return len(set(row)) == 1 and row[0] != EMPTY