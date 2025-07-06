import cv2
import numpy as np
import mediapipe as mp
import time

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Game variables
cell_size = 200  # Size of each cell for display
grid_size = 3  # Size of the grid (3x3)
symbols = ['X', 'O']

# Game board
board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
current_turn = 0  # 0 for Player 1, 1 for Player 2
players = ["Player 1", "Player 2"]  # Placeholder for player names
last_move = None  # To track the last move

# Define colors
colors = {
    "grid": (0, 0, 0),
    "highlight": (0, 255, 255),
    "X": (255, 0, 0),
    "O": (0, 255, 0),
    "text": (0, 0, 255)
}

def is_win(board, player_symbol):
    for i in range(grid_size):
        if all(board[i][j] == player_symbol for j in range(grid_size)) or \
           all(board[j][i] == player_symbol for j in range(grid_size)):
            return True
    if all(board[i][i] == player_symbol for i in range(grid_size)) or \
       all(board[i][grid_size - 1 - i] == player_symbol for i in range(grid_size)):
        return True
    return False

def is_draw(board):
    return all(all(cell is not None for cell in row) for row in board)

def is_valid_move(board, row, col):
    return board[row][col] is None

def play_turn(row, col):
    global current_turn, last_move
    if is_valid_move(board, row, col):
        board[row][col] = symbols[current_turn]
        last_move = (row, col)  # Track the last move
        if is_win(board, symbols[current_turn]):
            return f"{players[current_turn]} wins!"
        elif is_draw(board):
            return "It's a Draw!"
        current_turn = 1 - current_turn  # Switch turn
    return None

# Helper function to detect gestures
def detect_gesture(hand_landmarks):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    distance = np.sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)
    pinch_threshold = 0.05  # Adjust based on your requirements

    if distance < pinch_threshold:
        return "pinch"
    return None

# Main function
def main():
    global current_turn, last_move  # Ensure last_move is recognized as global
    cap = cv2.VideoCapture(0)

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    input_phase = True
    player_input_index = 0
    temp_name = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Handle name input phase
        if input_phase:
            prompt_text = f"Enter {players[player_input_index]} Name: {temp_name}_"
            cv2.putText(frame, prompt_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors["text"], 2)
            cv2.imshow("Tic Tac Toe", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('\r') or key == ord('\n'):  # Enter key to submit name
                players[player_input_index] = temp_name
                player_input_index += 1
                temp_name = ""
                if player_input_index >= 2:
                    input_phase = False
            elif key == ord('\b') and len(temp_name) > 0:  # Backspace to edit
                temp_name = temp_name[:-1]
            elif key != 255:  # Typing letters
                temp_name += chr(key)
            continue

        # Draw tic-tac-toe grid
        for i in range(1, grid_size):
            cv2.line(frame, (0, i * cell_size), (grid_size * cell_size, i * cell_size), colors["grid"], 2)
            cv2.line(frame, (i * cell_size, 0), (i * cell_size, grid_size * cell_size), colors["grid"], 2)

        # Draw current board state
        for i in range(grid_size):
            for j in range(grid_size):
                if board[i][j] == 'X':
                    cv2.putText(frame, 'X', (j * cell_size + 20, i * cell_size + 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, colors["X"], 5)
                elif board[i][j] == 'O':
                    cv2.putText(frame, 'O', (j * cell_size + 20, i * cell_size + 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, colors["O"], 5)

        # Detect hands and track finger positions
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect gesture
                gesture = detect_gesture(hand_landmarks)
                finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(finger_tip.x * w), int(finger_tip.y * h)
                row, col = y // cell_size, x // cell_size

                # Highlight cell for the index finger position
                if 0 <= row < grid_size and 0 <= col < grid_size:
                    cv2.rectangle(frame, (col * cell_size, row * cell_size),
                                  ((col + 1) * cell_size, (row + 1) * cell_size), colors["highlight"], 2)

                    # Place symbol only if pinch gesture detected over an empty cell
                    if gesture == "pinch" and is_valid_move(board, row, col):
                        result = play_turn(row, col)
                        time.sleep(0.5)  # Add delay to prevent multiple placements

                        if result:
                            # Show the result of the game
                            cv2.putText(frame, result, (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, colors["text"], 2)
                            cv2.putText(frame, "Press 'r' to play again or 'q' to quit", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors["text"], 2)
                            cv2.imshow("Tic Tac Toe", frame)
                            cv2.waitKey(2000)  # Wait to show the result

                            # Highlight the last move
                            if last_move:
                                row, col = last_move
                                cv2.rectangle(frame, (col * cell_size, row * cell_size),
                                              ((col + 1) * cell_size, (row + 1) * cell_size), colors["highlight"], 2)
                                cv2.putText(frame, symbols[current_turn], (col * cell_size + 20, row * cell_size + 80),
                                            cv2.FONT_HERSHEY_SIMPLEX, 3, colors[symbols[current_turn]], 5)
                            cv2.imshow("Tic Tac Toe", frame)

                            # Ask for user input to play again or quit
                            while True:
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord('r'):  # Reset game
                                    board[:] = [[None for _ in range(grid_size)] for _ in range(grid_size)]
                                    current_turn = 0
                                    last_move = None  # Reset last_move when starting a new game
                                    break
                                elif key == ord('q'):  # Quit game
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return

        # Show current player turn
        instruction_text = f"{players[current_turn]}'s Turn ({symbols[current_turn]})"
        cv2.putText(frame, instruction_text, (10, grid_size * cell_size + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors["text"], 2)

        # Show the frame
        cv2.imshow("Tic Tac Toe", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the game
if __name__ == "__main__":
    main()
