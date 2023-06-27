import cv2
import threading
import copy
import time
from cvzone.HandTrackingModule import HandDetector
import numpy as np

WIDTH, HEIGHT = 1280, 720
# Abstand zum bildschirmrand
margin = 100

target_x_min = -120
target_x_max = 120
target_y_min = -120
target_y_max = 120

class Detector:
    def __init__(self):
        cap = cv2.VideoCapture(0)
        # For mac we had to use different Camera Device
        #cap = cv2.VideoCapture(1)
        print("Video Captured")
        cap.set(3, WIDTH)
        cap.set(4, HEIGHT)
        self.width=1280
        self.height=720
        self.cap=cap
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.is_running = True
        self.hands=None
        self.hands_lock = threading.Lock()


    def start(self):
        # Starte den Webcam-Stream in einem separaten Thread
        webcam_thread = threading.Thread(target=self.run)
        webcam_thread.start()
  
    def run(self):
        webcam_thread = threading.Thread(target=self._detect_gesture)
        webcam_thread.start()

        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            with self.hands_lock:
                self.hands, img = self.detector.findHands(img, flipType=False)
            
            cv2.imshow("Webcam", img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        self.is_running = False
        webcam_thread.join()

    def _detect_gesture(self):
        try:            
            while self.is_running:
                with self.hands_lock:
                    hands_copy = copy.deepcopy(self.hands)
                if hands_copy:
                    if len(hands_copy) == 1:
                        self.one_hand_detection(hands_copy)
                    elif len(hands_copy) == 2:
                        self.two_hand_detection(hands_copy)
        except Exception as e:
            print("An error occured while detecting hand gesture.", e)
            print("Press q to end programm.")
            print("Error...retry...(Wait for 5 seconds)")
            time.sleep(5)
            self._detect_gesture()

    def one_hand_detection(self, hands_copy):
        # Get first hand (only one activated)
        hand = hands_copy[0]
        fingers = self.detector.fingersUp(hand)
        #print(fingers)
        #time.sleep(1)
        if fingers == [1, 1, 0, 0, 0]:
            self.one_index_finger_up(hand)
            
    def two_hand_detection(self, hands_copy):
        hand1, hand2 = hands_copy
        fingers1 = self.detector.fingersUp(hand1)
        fingers2 = self.detector.fingersUp(hand2)
        #print(fingers1+fingers2)
       # time.sleep(1)
        if fingers1 == [1, 1, 0, 0, 0] and fingers2 == [1, 1, 0, 0, 0]:
            self.two_index_fingers_up(hand1, hand2)
        if fingers1 == [0, 0, 0, 0, 0] and fingers2 == [0, 0, 0, 0, 0]:
            self.two_all_fingers_down(hand1, hand2)

    def one_index_finger_up(self, hand):
        pass

    def two_index_fingers_up(self, hand1, hand2):
        pass

    def two_all_fingers_down(self, hand1, hand2):
        pass