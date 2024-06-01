import cv2
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
prev_x = None
prev_y = None
prev_dist_left = None  # Added this line to store the previous distance between thumb and index finger for left hand
prev_dist_right = None  # Added this line to store the previous distance between thumb and index finger for right hand

while cap.isOpened():
    ret, frame = cap.read()

    # mirror image
    frame = cv2.flip(frame, 1)

    # Convert to rgb
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            handedness = results.multi_handedness[results.multi_hand_landmarks.index(landmarks)].classification[0].label

            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # Added this line to get the thumb tip landmark

            # Calculate the distance between the thumb tip and the index finger tip
            dist = math.sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)

            if handedness == "Left":
                mcp_x = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                mcp_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                scaling_factor = 1

                cursor_x = int(mcp_x * screen_width * scaling_factor)
                cursor_y = int(mcp_y * screen_height * scaling_factor)

                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                if index_tip.y >= landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                    pyautogui.click()

                # Added scrolling feature for left hand
                if prev_dist_left is not None:
                    if dist > prev_dist_left + 0.01:  # If the distance increased, scroll up
                        pyautogui.scroll(1)
                    elif dist < prev_dist_left - 0.01:  # If the distance decreased, scroll down
                        pyautogui.scroll(-1)

                prev_dist_left = dist

            elif handedness == "Right":
                x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)

                # Added zoom in and zoom out feature for right hand
                if prev_dist_right is not None:
                    if dist > prev_dist_right + 0.01:  # If the distance increased, zoom in
                        pyautogui.hotkey('ctrl', '+')
                    elif dist < prev_dist_right - 0.01:  # If the distance decreased, zoom out
                        pyautogui.hotkey('ctrl', '-')

                prev_dist_right = dist

                if prev_x is not None and prev_y is not None:
                    dx = x - prev_x
                    dy = y - prev_y

                    if abs(dx) > abs(dy):
                        if dx > 50:
                            pyautogui.press('right')
                        elif dx < -50:
                            pyautogui.press('left')
                    else:
                        if dy > 50:
                            pyautogui.press('down')
                        elif dy < -50:
                            pyautogui.press('up')

                prev_x = x
                prev_y = y

    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
