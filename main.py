import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt
import win32api
import pyautogui

# This is a python project based on ML for Virtual Mouse Tracking.

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Declaring a click variable which is to be use in the End.
click=0


# Taking input from Web Cam or any video capturing device.
video = cv2.VideoCapture(0)

# Sensitivity of feature detection Hands.  
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
  while video.isOpened():
    # GEtting video from the web cam.
    _, frame = video.read()   
    # OpenCV uses BGR & mediapipe uses RGB, We have to convert BGR to RGB to let Mediapipe work as shown below:-
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image,1)
    imageHeight, imageWidth, _ = image.shape
    results = hands.process(image)
    # converting RGB to BGR so that OpenCV can use it. 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Drawing of Landmarks and coordinates of Hand.
    if results.multi_hand_landmarks:
      for num, hand in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(250,44,250), thickness = 2, circle_radius=2),
                                   )

    # pixel coordinates of Index Finger and Thumb, Index finger for movement of cursor & Index finger and Thumb for "Clicking".
    if results.multi_hand_landmarks !=None:
      for handLandmarks in results.multi_hand_landmarks:
        for point in mp_hands.HandLandmark:


          # X and Y coordinates and Height and Width of frame.
          normalizedLandmark = handLandmarks.landmark[point]
          pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)


          # converting Specific datatype into String so that we can use it.
          point = str(point)

          if point == 'HandLandmark.INDEX_FINGER_TIP':
            try:
              indexfingertip_x=pixelCoordinatesLandmark[0]
              indexfingertip_y=pixelCoordinatesLandmark[1]
              # using win32api to set cursor position, multiplying indexes with 4 & 5 so that during movement of hand cursor can move to bigger Range. 
              win32api.SetCursorPos((indexfingertip_x*4,indexfingertip_y*5))

            except:
              pass

          elif point=='HandLandmark.THUMB_TIP':
            try:
              thumbfingertip_x=pixelCoordinatesLandmark[0]
              thumbfingertip_y=pixelCoordinatesLandmark[1]
              #print("thumb",thumbfingertip_x)
              
            except:
              pass

          try:
            # Calculate the distance between Index Finger Tip and Thumb Finger Tip for X and Y.
            Distance_x=sqrt((indexfingertip_x-thumbfingertip_x)**2 + (indexfingertip_x-thumbfingertip_x)**2)
            Distance_y=sqrt((indexfingertip_y-thumbfingertip_y)**2 + (indexfingertip_y-thumbfingertip_y)**2)
            if Distance_x<5 or Distance_x<-5:
              if Distance_y<5 or Distance_y<-5:
                click=click+1
                if click%5==0:
                  print("Single Click")
                  # pyautogui works only if the clicks are in multiple or in factorial of 5, so it will reduce the clicks and gets clicked once, when you move fingers away.
                  pyautogui.click()
          except:
            pass

    # Returning output stream to user using cv2.imshow & exit condition using cv2.waitKey add order q and Break gets executed.
    cv2.imshow('Movement Tracking of Hand', image)
    if cv2.waitKey(10) & 0xFF ==ord('q'):
      break

# Now the video gets stopped and all windows get terminated by using distroyallWindows.
video.release()
cv2.distroyAllWindows()