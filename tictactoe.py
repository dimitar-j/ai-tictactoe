"""
Tic Tac Toe Player
"""

import math
from random import choice
from multiprocessing.sharedctypes import Value

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
    x_count = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == X:
                x_count += 1
            if board[r][c] == O:
                x_count -= 1
    if x_count > 0: return O
    else: return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == EMPTY:
                actions.add((r,c))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check for valid cell input
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        return ValueError
    if board[action[0]][action[1]]: # cell already filled
        return ValueError

    # make a deep copy for new board
    new_board = initial_state()
    for r in range(len(board)):
        for c in range(len(board[r])):
            new_board[r][c] = board[r][c]
    
    current_turn = player(board)
    new_board[action[0]][action[1]] = current_turn

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for a winning horizontal row
    for r in range(len(board)):
        if board[r][0] == board[r][1] and board[r][1] == board[r][2] and board[r][0]:
            return board[r][0]
    # Check for a winning vertical row
    for c in range(len(board)):
        if board[0][c] == board[1][c] and board[1][c] == board[2][c] and board[0][c]:
            return board[0][c]
    # Check for a winning diagnoal row
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][0]:
        return board[0][2]
    return None # No winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner, game is over
    if winner(board): return True
    # if no winner and an empty cell exists, game is not over
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == EMPTY:
                return False
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    if result == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)
    outcomes = set() # keep track of each outcome caused by each action
    for action in actions(board):
        if current_player == X:
            outcome = minvalue(result(board,action))
        else:
            outcome = maxvalue(result(board,action))
        outcomes.add((outcome,action))
    if current_player == X:
        m = max(outcomes, key=lambda item:item[0])
    else:
        m = min(outcomes, key=lambda item:item[0])
    optimal_outcome = [choice([j for j in outcomes if j[0] == m[0]])]
    return optimal_outcome[0][1]
    

def maxvalue(board):
    """
    Returns the highest outcome possible with the given board
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minvalue(result(board,action)))
    return v

def minvalue(board):
    """
    Returns the lowest outcome possible with the given board
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxvalue(result(board,action)))
    return v

