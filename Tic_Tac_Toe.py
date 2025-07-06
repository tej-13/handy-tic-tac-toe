"""
Contain All Tic Tac Toe major functions
"""

import numpy as np
import mediapipe as mp
import tkinter as tk

# Function to initialize the game board and turn
def initialization():
    """
    Initialize the game board and starting turn.

    Returns:
        tuple: A tuple containing the initialized board (3x3 grid of None) and starting turn (0 for player).
    """
    board = [[None for _ in range(3)] for _ in range(3)]  # Initialize empty board
    turn = 0  # Player's turn
    return board, turn

# Function to check for a win condition
def is_win(board, player_symbol):
    """
    Check if the given player has won the game.

    Args:
        board (list): The current game board.
        player_symbol (str): The symbol of the player ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check rows for matching symbols
    for ri in range(3):
        if all(board[ri][ci] == player_symbol for ci in range(3)):
            return True
    # Check columns for matching symbols
    for ci in range(3):
        if all(board[ri][ci] == player_symbol for ri in range(3)):
            return True
    # Check diagonals for matching symbols
    if all(board[i][i] == player_symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == player_symbol for i in range(3)):
        return True
    return False

# Function to check if the game is a draw
def is_draw(board):
    """
    Check if the game is a draw (i.e., all cells are filled and there is no winner).

    Args:
        board (list): The current game board.

    Returns:
        bool: True if the game is a draw, False otherwise.
    """
    # Check if all cells are filled with X or O
    return all(all(cell is not None for cell in row) for row in board)

# Function to determine if a move is valid
def is_valid_move(board, ri, ci):
    """
    Check if a move is valid (i.e., the selected cell is empty).

    Args:
        board (list): The current game board.
        ri (int): The row index of the move.
        ci (int): The column index of the move.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return board[ri][ci] is None

# Alpha-Beta Pruning algorithm to evaluate game states
def alpha_beta(board, depth, alpha, beta, is_maximizing, cs, ps):
    """
    Alpha-Beta Pruning algorithm to evaluate game states and determine the optimal move.

    Args:
        board (list): The current game board.
        depth (int): The current depth in the game tree.
        alpha (float): The best value that the maximizer can guarantee.
        beta (float): The best value that the minimizer can guarantee.
        is_maximizing (bool): Flag indicating if the current turn is maximizing or minimizing.
        cs (str): The symbol of the computer ('X' or 'O').
        ps (str): The symbol of the player ('X' or 'O').

    Returns:
        int: The evaluation score of the current game state.
    """
    # Check for terminal states (win/loss/draw) and return their scores
    if is_win(board, cs):
        return 1
    if is_win(board, ps):
        return -1
    if is_draw(board):
        return 0

    # Maximizing player's turn
    if is_maximizing:
        max_eval = -float('inf')
        for r in range(3):
            for c in range(3):
                if is_valid_move(board, r, c):
                    board[r][c] = cs
                    eval = alpha_beta(board, depth + 1, alpha, beta, False, cs, ps)
                    board[r][c] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    # Minimizing player's turn
    else:
        min_eval = float('inf')
        for r in range(3):
            for c in range(3):
                if is_valid_move(board, r, c):
                    board[r][c] = ps
                    eval = alpha_beta(board, depth + 1, alpha, beta, True, cs, ps)
                    board[r][c] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to determine the computer's move using Alpha-Beta Pruning
def computer_move(board, cs, ps):
    """
    Determine the optimal move for the computer using the Alpha-Beta Pruning algorithm.

    Args:
        board (list): The current game board.
        cs (str): The symbol of the computer ('X' or 'O').
        ps (str): The symbol of the player ('X' or 'O').

    Returns:
        tuple: The best move as a tuple (row, column) or None if no valid move is found.
    """
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if is_valid_move(board, r, c):
                board[r][c] = cs
                score = alpha_beta(board, 0, -float('inf'), float('inf'), False, cs, ps)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move


