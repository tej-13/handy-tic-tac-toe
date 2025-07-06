"Handy Tic Tac Toe"
import mediapipe as mp
import cv2 
import numpy as np
import Tic_Tac_Toe as ttt
import Helper_Functions as helper



# Main function to run the Tic Tac Toe game
def main():
    # Open the webcam
    cap = helper.Open_Video_Frame()  
    player_name = ''  # Variable to store player name
    player_symbol = ['X', 'O']  # Symbols for player and computer
    typing_active = True  # Flag to manage player name input
    board, turn = ttt.initialization()  # Initialize game board and starting turn
    window_width, window_height = helper.get_window_height_and_width()  # Get dimensions of the window
    pointed_cell = None  # Currently pointed cell by the player's finger
    stable_cell = None  # Stable cell selected by the player's finger
    stable_count = 0  # Count of stable frames for finger position
    required_stable_frames = 30  # Number of stable frames required to confirm cell selection

    # Initialize MediaPipe Hands module
    mp_hands = mp.solutions.hands  
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)  # Configure Hands instance
    mp_draw = mp.solutions.drawing_utils  # MediaPipe drawing utilities

    #Loading screen
    display_screen = np.zeros((1080, 640, 3), np.uint8)
    helper.display_message("Tic Tac Toe", display_screen, position=(50, 400), font_scale=3 )
    helper.display_message("Loading......", display_screen, position=(50, 650), font_scale=3 )
    cv2.namedWindow('Initial Window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Initial Window', 1080, 640)
    cv2.imshow('Initial Window', display_screen)
    cv2.waitKey(5000)  
    cv2.destroyWindow('Initial Window')

    # Main game loop
    while True:
        ret, frame = cap.read()  # Read frame from webcam
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        height, width = frame.shape[:2]  # Get frame dimensions
        Initial_frame = np.zeros((window_height + 200, window_width + 200, 3), np.uint8)  # Blank initial frame
        Canvas = np.zeros((300, 300, 3), np.uint8)  # Blank canvas for game grid
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
        result = hands.process(frame_rgb)  # Process hand landmarks

        # Draw hand landmarks on frame if detected
        if result.multi_hand_landmarks:  
            hand_landmarks = result.multi_hand_landmarks[0]  # Get first hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # Draw hand landmarks

            # Get coordinates of the tip of the index finger
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # Convert to pixel coordinates
            cx, cy = int(index_finger_tip.x * width), int(index_finger_tip.y * height)  
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)  # Draw circle at finger tip

            # Determine which cell is pointed by the index finger
            pointed_cell = helper.get_cell_number(frame, (cx, cy))  

            # Check if the finger is pointing to the same cell stably
            if stable_cell == pointed_cell:
                stable_count += 1
            else:
                stable_cell = pointed_cell
                stable_count = 0

            # Confirm cell selection if pointed stably for required frames
            if stable_count > required_stable_frames:
                row, col = divmod(stable_cell, 3)
                if ttt.is_valid_move(board, row, col):
                    board[row][col] = player_symbol[turn]  # Update board with player's move
                    turn ^= 1  # Switch turn
                    stable_cell = None  # Reset stable cell
                    stable_count = 0

        # Draw game grid and marks on Canvas and frame
        Canvas = helper.draw_grid(Canvas)
        frame = helper.draw_grid(frame)
        Canvas = helper.draw_marks(Canvas, board)
        frame = helper.draw_marks(frame, board)
        copy_frame = frame.copy()  # Create a copy of the frame

        # Configure display window for webcam frame
        cv2.namedWindow('Webcam Frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Webcam Frame', window_width + 200, window_height + 200)

        # Handle player name input
        if typing_active:  
            helper.display_message("Enter Your Name :", Initial_frame, position=(window_height // 5, window_width // 6), font_scale=2, color=(0, 150, 0), thickness=3)
            helper.display_message(player_name, Initial_frame, position=(window_height // 2, window_width // 2), font_scale=1, color=(139, 0, 0), thickness=2)
            cv2.imshow('Webcam Frame', Initial_frame)
            key = cv2.waitKey(1)  # Wait for key press
            if key == 13 and player_name:  # Enter key pressed and name is non-empty
                typing_active = False  # Deactivate name input
            elif key != -1:
                player_name = helper.update_text(key, player_name)  # Update player name

        else:  # Handle game turns
            if turn == 0:  # Player's turn
                helper.display_message(f"{player_name}'s Turn", frame, position=(50, 100), font_scale=2)
                cv2.imshow('Webcam Frame', frame)
            else:  # Computer's turn
                helper.display_message("Computer's Turn", frame, position=(50, 100), font_scale=2)
                computer_move_pos = ttt.computer_move(board, player_symbol[1], player_symbol[0])  # Get computer's move
                if computer_move_pos:
                    board[computer_move_pos[0]][computer_move_pos[1]] = player_symbol[turn]  # Update board with computer's move
                    turn ^= 1  # Switch turn

        # Display Tic Tac Toe grid
        cv2.imshow('Tic Tac Toe', Canvas)

        # Check game status for win, lose, or draw
        if ttt.is_win(board, player_symbol[0]):  # Player wins
            Canvas = helper.draw_marks(Canvas, board)
            frame = helper.draw_marks(copy_frame, board)
            helper.display_message(f"{player_name} Wins!", copy_frame, position=(50, 300), font_scale=2)
            cv2.imshow('Webcam Frame', copy_frame) 
            cv2.imshow('Tic Tac Toe', Canvas)
            cv2.waitKey(5000)
            break
        elif ttt.is_win(board, player_symbol[1]):  # Computer wins
            Canvas = helper.draw_marks(Canvas, board)
            frame = helper.draw_marks(copy_frame, board)
            helper.display_message("Computer Wins!", copy_frame, position=(50, 300), font_scale=2)
            cv2.imshow('Webcam Frame', copy_frame)
            cv2.imshow('Tic Tac Toe', Canvas)
            cv2.waitKey(5000)
            break
        elif ttt.is_draw(board):  # Draw game
            Canvas = helper.draw_marks(Canvas, board)
            frame = helper.draw_marks(copy_frame, board)
            helper.display_message("Draw!", copy_frame, position=(200, 300), font_scale=3)
            cv2.imshow('Webcam Frame', copy_frame)
            cv2.imshow('Tic Tac Toe', Canvas)
            cv2.waitKey(5000)
            break

        # Exit game on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function if the script is executed
if __name__ == "__main__":
    main()

