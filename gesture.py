import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

width, height = 1280, 720


cap = cv2.VideoCapture(0)
print("Video Captured")
cap.set(3, width)
cap.set(4, height)

# Detect hand
# detection con: wie sicher ist das programm, dass es eine hand ist? 80 prozent
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Abstand zum bildschirmrand
margin = 100

target_x_min = -120
target_x_max = 120
target_y_min = -120
target_y_max = 120


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        # Get first hand (only one activated)
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers == [1, 1, 0, 0, 0]:
            lmList = hand["lmList"]
            indexFinger = lmList[8][0], lmList[8][1], lmList[8][2]
            index_finger_x = lmList[8][0]
            index_finger_y = lmList[8][1]
            index_finger_z = lmList[8][2]

            normalized_x = (index_finger_x - margin) / (width - 2 * margin)
            mapped_x = int(target_x_min +
                           (target_x_max - target_x_min) * normalized_x)

            normalized_y = (index_finger_y - margin) / (height - 2 * margin)
            mapped_y = int(target_y_min +
                           (target_y_max - target_y_min) * normalized_y)

            zVal = index_finger_z

            print(
                f"x: {lmList[8][0]}, y: {lmList[8][1]}, z: {lmList[8][2]} \t\t -> \t\t x:{mapped_x}, y: {mapped_y}, z: {zVal}")

    cv2.imshow("Webcam", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
