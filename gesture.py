import cv2
from cvzone.HandTrackingModule import HandDetector


width, height = 1280, 720


cap = cv2.VideoCapture(0)
print("Video Captured")
cap.set(3, width)
cap.set(4, height)

# Detect hand
# detection con: wie sicher ist das programm, dass es eine hand ist? 80 prozent
detector = HandDetector(detectionCon=0.8, maxHands=1)

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
            print(indexFinger)

    cv2.imshow("Webcam", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
