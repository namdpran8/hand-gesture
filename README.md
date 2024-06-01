# hand-gesture

Gesture Recognition System using Hand Landmarks: This code captures video from the webcam, detects hand landmarks using the mediapipe library, and performs actions based on hand gestures. Here’s what it does:

Initialization:
  Imports necessary libraries (cv2, mediapipe, and pyautogui).
  Sets up webcam capture and screen dimensions.
  
Hand Detection:
  Uses mediapipe to detect hand landmarks in each frame.
  Determines handedness (left or right) of the detected hand.
  
Left Hand Actions:
  If the detected hand is left:
  Calculates cursor position based on middle finger metacarpal (MCP) landmark.
  Moves cursor using pyautogui.moveTo().
  Simulates mouse click if index finger tip is below index finger middle joint.
  
Right Hand Actions:
  If the detected hand is right:
  Calculates cursor position based on index finger tip landmark.
  Determines movement direction (horizontal or vertical) based on cursor position change.
  Simulates arrow key presses ('right', 'left', 'up', or 'down') using pyautogui.press().
  
Display and Exit:
  Displays processed frame with hand landmarks.
  Pressing ‘q’ quits the program.
