import threading
import copy
import time
import cv2
from cvzone.HandTrackingModule import HandDetector

# Size of camera picture
WIDTH, HEIGHT = 1280, 720

class Detector:
    """
    A class for detecting hand gestures using a webcam.
    """

    def __init__(self):
        cap = cv2.VideoCapture(0)
        # For Mac, we had to use a different camera device
        # cap = cv2.VideoCapture(1)
        print("Video Captured")
        cap.set(3, WIDTH)
        cap.set(4, HEIGHT)
        self.width = 1280
        self.height = 720
        self.cap = cap
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.is_running = True
        self.hands = None
        self.hands_lock = threading.Lock()

    def start(self):
        """
        Start the webcam stream in a separate thread.
        """
        webcam_thread = threading.Thread(target=self.run)
        webcam_thread.start()

    def run(self):
        """
        Run the webcam stream and hand gesture detection.
        """
        webcam_thread = threading.Thread(target=self._detect_gesture)
        webcam_thread.start()

        while True:
            _, img = self.cap.read()
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
        """
        Perform hand gesture detection.
        """
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
            print("An error occurred while detecting hand gesture:", e)
            print("Press 'q' to end the program.")
            print("Error... retry... (Waiting for 5 seconds)")
            time.sleep(5)
            self._detect_gesture()

    def one_hand_detection(self, hands_copy):
        """
        Detect gestures that work only when one hand is detected.

        Args:
            hands_copy (list): A list containing the detected hand(s).
        """
        # Get the first hand (only one activated)
        hand = hands_copy[0]
        fingers = self.detector.fingersUp(hand)
        # print(fingers)
        # time.sleep(1)
        if fingers == [1, 1, 0, 0, 0]:
            self.one_index_finger_up(hand)

    def two_hand_detection(self, hands_copy):
        """
        Detect gestures that work only when two hands are detected.

        Args:
            hands_copy (list): A list containing the detected hand(s).
        """
        # Get the two hands
        hand1, hand2 = hands_copy
        fingers1 = self.detector.fingersUp(hand1)
        fingers2 = self.detector.fingersUp(hand2)
        if fingers1 == [1, 1, 0, 0, 0] and fingers2 == [1, 1, 0, 0, 0]:
            self.two_index_fingers_up(hand1, hand2)
        if fingers1 == [0, 0, 0, 0, 0] and fingers2 == [0, 0, 0, 0, 0]:
            self.two_all_fingers_down(hand1, hand2)

    def one_index_finger_up(self, hand):
        """
        Handle the gesture when one index finger is up.

        Args:
            hand: The detected hand.
        """
        pass

    def two_index_fingers_up(self, hand1, hand2):
        """
        Handle the gesture when two index fingers are up.

        Args:
            hand1: The first detected hand.
            hand2: The second detected hand.
        """
        pass

    def two_all_fingers_down(self, hand1, hand2):
        """
        Handle the gesture when all fingers are down for both hands.

        Args:
            hand1: The first detected hand.
            hand2: The second detected hand.
        """
        pass
