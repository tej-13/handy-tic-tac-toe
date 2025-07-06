# Handy Tic Tac Toe AI

This project implements a Tic Tac Toe game that can be played using hand gestures. The game uses OpenCV and MediaPipe for hand gesture detection, and an AI algorithm (Alpha-Beta Pruning) to determine the optimal moves for the computer.

## Features

- **Hand Gesture Recognition:** Play Tic Tac Toe by pointing to the desired cell with your index finger.
- **AI Opponent:** The computer uses the Alpha-Beta Pruning algorithm to make optimal moves.
- **Dynamic Grid Drawing:** The Tic Tac Toe grid and marks (X and O) are drawn dynamically on the video feed.
- **Win/Draw Detection:** The game detects win, draw, and loss conditions and displays appropriate messages.

## How to Play

1. **Start the Game:** Run the script and allow access to your webcam.
2. **Enter Your Name:** Type your name and press Enter.
3. **Player's Turn:** Use your index finger to point at the cell where you want to place your mark (X). Hold your finger steadily over the cell for a few seconds to confirm your move.
4. **Computer's Turn:** The AI opponent will make its move.
5. **Win, Lose, or Draw:** The game will display a message indicating the result. You can restart the game or exit.

## Project Structure

1. **Video Frame Initialization**
    - Opening and capturing video frames from the webcam.
    - Displaying messages on the frames.

2. **Hand Gesture Detection**
    - Using MediaPipe for hand tracking.
    - Processing hand landmarks to detect gestures.

3. **Game Mechanics**
    - Drawing the Tic Tac Toe grid.
    - Updating the game board based on player moves.
    - Implementing the AI opponent using Alpha-Beta Pruning.
    - Checking for win or draw conditions.

4. **AI Opponent**
    - Implementing the Alpha-Beta Pruning algorithm to evaluate game states and determine the optimal move.

5. **User Interface**
    - Displaying instructions and messages on the screen.
    - Handling player name input.
    - Visualizing game progress and results.

<!--
## Code Overview

- **Open_Video_Frame:** Opens the webcam for capturing video frames.
- **display_message:** Displays messages on the frame.
- **update_text:** Updates the text based on key presses.
- **get_window_height_and_width:** Gets the dimensions of the window.
- **draw_grid:** Draws the Tic Tac Toe grid on the given frame.
- **draw_marks:** Draws the X and O marks on the Tic Tac Toe board.
- **get_cell_number:** Gets the cell number based on the index finger coordinates.
- **initialization:** Initializes the game board and starting turn.
- **is_win:** Checks if a player has won the game.
- **is_draw:** Checks if the game is a draw.
- **is_valid_move:** Determines if a move is valid.
- **alpha_beta:** Implements the Alpha-Beta Pruning algorithm to evaluate game states.
- **computer_move:** Determines the computer's optimal move using the Alpha-Beta Pruning algorithm.
- **main:** The main function to run the Tic Tac Toe game.
-->



## Gameplay Demonstration

### Loading Screen
<img width="500" src="assets/Loading Screen.PNG" alt="loading"/>


### Game in Action
<img width="500" src="assets/Action.PNG" alt="action"/>

### Endgame Summary
<img width="500" src="assets/Result.PNG" alt="result"/>


## References

- [OpenCV Documentation](https://docs.opencv.org/)
- [MediaPipe Documentation](https://mediapipe.dev/)
