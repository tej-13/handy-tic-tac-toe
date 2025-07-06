"""
Contain all helper functions
"""

import cv2
import numpy as np
import mediapipe as mp
import tkinter as tk

# Function to open the video frame
def Open_Video_Frame():
    """
    Open the webcam for capturing video frames.

    Returns:
        cap (cv2.VideoCapture): VideoCapture object for the webcam.
    """
    cap = cv2.VideoCapture(0)  # Open the default webcam
    if not cap.isOpened():  # Check if the webcam opened successfully
        print("Error: Could not open webcam.")
    else:
        print("Webcam opened successfully.")
    return cap

# Function to display a message on the frame
def display_message(message, frame, position=(50, 50), font_scale=3, color=(255, 255, 255), thickness=2):
    """
    Display a message on the given frame.

    Args:
        message (str): The message to display.
        frame (np.ndarray): The frame on which to display the message.
        position (tuple): The position (x, y) to display the message.
        font_scale (int): The scale of the font.
        color (tuple): The color of the text in BGR format.
        thickness (int): The thickness of the text.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX  # Use the Hershey Simplex font
    cv2.putText(frame, message, position, font, font_scale, color, thickness, cv2.LINE_AA)  # Draw the text on the frame

# Function to update text based on key presses
def update_text(key, typed_text):
    """
    Update the text based on key presses.

    Args:
        key (int): The ASCII value of the key pressed.
        typed_text (str): The current text that has been typed.

    Returns:
        str: The updated text after processing the key press.
    """
    if key == 8:  # Backspace key
        typed_text = typed_text[:-1]  # Remove the last character
    else:
        typed_text += chr(key)  # Add the typed character to the text
    return typed_text

# Function to get the window height and width
def get_window_height_and_width():
    """
    Get the dimensions of the window.

    Returns:
        tuple: The width and height of the window.
    """
    # Create a temporary Tkinter window to get screen dimensions
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # Destroy the temporary window

    # Calculate window dimensions as half of screen dimensions
    window_width = screen_width // 2
    window_height = screen_height // 2
    return window_width, window_height

# Function to draw the tic-tac-toe grid
def draw_grid(frame):
    """
    Draw the tic-tac-toe grid on the given frame.

    Args:
        frame (np.ndarray): The frame on which to draw the grid.

    Returns:
        np.ndarray: The frame with the grid drawn on it.
    """
    height, width = frame.shape[:2]
    cell_h = height // 3
    cell_w = width // 3
    x1, x2 = cell_w, 2 * cell_w
    y1, y2 = cell_h, 2 * cell_h

    # Draw grid lines
    cv2.line(frame, (x1, 0), (x1, height), (139, 0, 0), 2)  # Vertical line 1
    cv2.line(frame, (x2, 0), (x2, height), (139, 0, 0), 2)  # Vertical line 2
    cv2.line(frame, (0, y1), (width, y1), (139, 0, 0), 2)  # Horizontal line 1
    cv2.line(frame, (0, y2), (width, y2), (139, 0, 0), 2)  # Horizontal line 2
    return frame

# Function to draw the marks on the tic-tac-toe board
def draw_marks(frame, board):
    """
    Draw the X and O marks on the tic-tac-toe board.

    Args:
        frame (np.ndarray): The frame on which to draw the marks.
        board (list): The current state of the board.

    Returns:
        np.ndarray: The frame with the marks drawn on it.
    """
    height, width = frame.shape[:2]
    cell_h = height // 3
    cell_w = width // 3

    # Draw X or O marks on the board
    for row in range(3):
        for col in range(3):
            mark = board[row][col]
            if mark is not None:
                center_x = int(col * cell_w + cell_w // 2)
                center_y = int(row * cell_h + cell_h // 2)
                center = (center_x, center_y)
                if mark == 'X':
                    # Draw X
                    cv2.line(frame, (center[0] - cell_w // 4, center[1] - cell_h // 4), 
                             (center[0] + cell_w // 4, center[1] + cell_h // 4), (255, 0, 0), 2)
                    cv2.line(frame, (center[0] + cell_w // 4, center[1] - cell_h // 4), 
                             (center[0] - cell_w // 4, center[1] + cell_h // 4), (255, 0, 0), 2)
                elif mark == 'O':
                    # Draw O
                    cv2.circle(frame, center, cell_w // 4, (0, 255, 0), 2)
    return frame

# Function to get the cell number based on the index finger coordinates
def get_cell_number(frame, coordinate_of_index):
    """
    Get the cell number based on the index finger coordinates.

    Args:
        frame (np.ndarray): The frame from the webcam.
        coordinate_of_index (tuple): The (x, y) coordinates of the index finger.

    Returns:
        int: The cell number (0-8) based on the index finger position.
    """
    height, width = frame.shape[:2]
    cell_h = height // 3
    cell_w = width // 3
    x, y = coordinate_of_index

    # Determine row and column of the cell based on finger position
    col = x // cell_w
    row = y // cell_h

    # Ensure cell number is within bounds
    if row >= 3:
        row = 2
    if col >= 3:
        col = 2

    cell_number = row * 3 + col  # Calculate the cell number
    return cell_number