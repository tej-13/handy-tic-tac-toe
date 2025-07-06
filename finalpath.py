import tkinter as tk
from tkinter import messagebox
import threading
import os

# Import your game functions
import Handy_Tic_Tac_Toe as game

# Start the game in a new thread
def start_game():
    threading.Thread(target=game.main).start()

# Show game instructions
def show_instructions():
    instructions = """
    Handy Tic Tac Toe Instructions:
    
    1. Use your index finger to point to the grid cells.
    2. Keep your finger steady for a few seconds to select a cell.
    3. Your goal is to align three symbols (X or O) in a row, column, or diagonal.
    4. You can quit anytime by pressing 'quit'.
    
    Have fun playing!
    """
    messagebox.showinfo("Instructions", instructions)



# Main window setup
root = tk.Tk()
root.title("Handy Tic Tac Toe")
root.geometry("400x300")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Handy Tic Tac Toe", font=("Helvetica", 16, "bold"))
title.pack(pady=20)

# Buttons
start_button = tk.Button(root, text="Start Game", command=start_game, width=15, bg="#4CAF50", fg="white")
start_button.pack(pady=10)

instructions_button = tk.Button(root, text="Instructions", command=show_instructions, width=15, bg="#2196F3", fg="white")
instructions_button.pack(pady=10)




quit_button = tk.Button(root, text="Quit", command=root.quit, width=15, bg="#F44336", fg="white")
quit_button.pack(pady=10)

# Run the frontend
root.mainloop()
