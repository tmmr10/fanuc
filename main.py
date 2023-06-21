import time
from gesture.communicator import Communicator
from gesture.detector import Detector

HOST_ADDR="10.215.255.151"
TCP_PORT=59002
margin = 100

target_x_min = -120
target_x_max = 120
target_y_min = -45
target_y_max = 52

class RobotDetector(Detector):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator
    
    def one_index_finger_up(self, hand):
        lmList = hand["lmList"]
        indexFinger = lmList[8][0], lmList[8][1], lmList[8][2]
        index_finger_x = lmList[8][0]
        index_finger_y = lmList[8][1]
        index_finger_z = lmList[8][2]

        normalized_x = (index_finger_x - margin) / (self.width - 2 * margin)
        mapped_x = int(min(target_x_max, max(target_x_min, target_x_min + (target_x_max - target_x_min) * normalized_x)))

        normalized_y = (index_finger_y - margin) / (self.height - 2 * margin)
        mapped_y = int(min(target_y_max, max(target_y_min, target_y_min + (target_y_max - target_y_min) * normalized_y)))
        zVal = index_finger_z
        #print(
        #   f"x: {lmList[8][0]}, y: {lmList[8][1]}, z: {lmList[8][2]} \t\t -> \t\t x:{mapped_x}, y: {mapped_y}, z: {zVal}")
        print( f"x : {mapped_x} , y: {mapped_y}, z:{zVal}")
        zVal=-22
        #mapped_x=50
        data= self.communicator.send_position(mapped_x, zVal, mapped_y)
        #print(data)
        print("one up")
        time.sleep(0.05)

    def two_index_fingers_up(self, hand1, hand2):
        print("both_up")
        #time.sleep(2)
    
    def two_all_fingers_down(self, hand1, hand2):
        print("all down")
        #time.sleep(2)
    
    #def index_finger_up(self, hand):
    #    print("Detected")
    #    time.sleep(1)


def main():
    communicator= Communicator(HOST_ADDR, TCP_PORT)
    communicator.connect_to_socket()
    #robot_detector= RobotDetector(communicator)
    try:
        print(communicator.get_position())
        #robot_detector.run()

    finally:
        print("none")
        communicator.close_connection()

def main1():
    communicator= Communicator(HOST_ADDR, TCP_PORT)
    communicator.connect_to_socket()
    try:
        #communicator.send_position(-105, 22, -22)
        #communicator.send_position(119, 22, -22)
        communicator.send_position(65, -96, -22)
        print(communicator.get_position())
    finally:
        
        communicator.close_connection()
    
    
if __name__ == "__main__":
    main()


# -40 29 -20;
# TODO: Fixen, wenn er kein ack zurückbekommt, soll quit trotzdem die session killen