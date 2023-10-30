"""
Tic Tac Toe Player
"""

import math

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

    REMEMBER TO ADD THE CASE IF THE GAME IS OVER HERE ONCE THAT FUNCTION IS IMPLEMENTED
    """
    if terminal(board):
        return "Game Over"
    else:
        board = [i for n in board for i in n]
        play_count = 9 - board.count(EMPTY)
        if play_count % 2 == 1:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                possible.add(tuple([row, col]))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action[0], action[1]
    board[i][j] = player(board)

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_combos = [{(0, 0), (0, 1), (0, 2)},
                  {(1, 0), (1, 1), (1, 2)},
                  {(2, 0), (2, 1), (2, 2)},
                  {(0, 0), (1, 0), (2, 0)},
                  {(0, 1), (1, 1), (2, 1)},
                  {(0, 2), (1, 2), (2, 2)},
                  {(0, 0), (1, 1), (2, 2)},
                  {(0, 2), (1, 1), (2, 0)}]

    x_combos = {0}
    o_combos = {0}

    for row in range(3):
        for col in range(3):
            if board[row][col] == X:
                x_combos.add(tuple([row, col]))
            elif board[row][col] == O:
                o_combos.add(tuple([row, col]))

    for combo in win_combos:
        if combo.issubset(x_combos):
            return X
        elif combo.issubset(o_combos):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if board.count(EMPTY) == 9:
        return True
    elif winner(board) is not None:
        return True
    else:
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
    if player(board) == X:
        MAX_VALUE(board)
    else:
        MIN_VALUE(board)

def MAX_VALUE(board):
    if terminal(board):
        return utility(board)
    current_best = -math.inf
    for action in actions(board):
        child_value = MIN_VALUE(result(board, action))
        if child_value > current_best:
            current_best = child_value
    return current_best

def MIN_VALUE(board):
    if terminal(board):
        return utility(board)
    current_worst = math.inf
    for action in actions(board):
        child_value = MAX_VALUE(result(board, action))
        if child_value < current_worst:
            current_worst = child_value
    return current_worst
