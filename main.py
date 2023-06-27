import time
from gesture.communicator import Communicator
from gesture.detector import Detector

HOST_ADDR="10.215.255.151"
TCP_PORT=59002

home_position=(65, -96, -22)
# margin is necessary because the detection at the screen edge does not work well
margin = 100

target_y_min = -119
target_y_max = 119
target_z_min = -44
target_z_max = 51


# Ungefähre z erkennung von bild( ist abhängig von Kamera)
z_detect_min =-240
z_detect_max= 0

target_x_min=-146
target_x_max= 50

class RobotDetector(Detector):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator
    
    def one_index_finger_up(self, hand):
        lmList = hand["lmList"]
        index_finger_x = lmList[8][0]
        index_finger_y = lmList[8][1]
        index_finger_z = lmList[8][2]

        # X coord image (==y on target)
        normalized_x = (index_finger_x - margin) / (self.width - 2 * margin)
        mapped_x = int(min(target_y_max, max(target_y_min, target_y_min + (target_y_max - target_y_min) * normalized_x)))

        # y coord image (==z on target)
        normalized_y = (index_finger_y - margin) / (self.height - 2 * margin)
        mapped_y = int(min(target_z_max, max(target_z_min, target_z_min + (target_z_max - target_z_min) * normalized_y)))
        
        normalized_z = (index_finger_z - z_detect_min) / (z_detect_max - z_detect_min)
        zVal = int(min(target_x_max, max(target_x_min, target_x_min + (target_x_max - target_x_min) * normalized_z)))
        #print(
        #   f"x: {lmList[8][0]}, y: {lmList[8][1]}, z: {lmList[8][2]} \t\t -> \t\t x:{mapped_x}, y: {mapped_y}, z: {zVal}")
        #print( f"x : {mapped_x} , y: {mapped_y}, z:{zVal}")
        #mapped_x=50
        print(f"Umapped: {index_finger_z}. Mapped: {zVal}")
        self.communicator.send_position(mapped_x, zVal, mapped_y)
        #print(data)
        #print("one up")
        time.sleep(0.05)

    def two_index_fingers_up(self, hand1, hand2):
        print("both_up")
        #time.sleep(2)
    
    def two_all_fingers_down(self, hand1, hand2):
        print("Go to home position")
        self.communicator.send_position(*home_position)
        position= self.communicator.get_position()
        
        print(position)
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < 10:
            coords = self.communicator.get_position().decode().split("|")
            rec_pos= tuple([float(coord) for coord in coords])
            if self._compare_positions(
                home_position, rec_pos, 0.1):
                print("Positions match")
                break
            elapsed_time = time.time() - start_time
            
        
    def _compare_positions(self, sent_pos, rec_pos, threshold):
        for i in range(3):
            if abs(sent_pos[i] - rec_pos[i]) > threshold:
                return False
        return True

def main():
    communicator= Communicator(HOST_ADDR, TCP_PORT)
    communicator.connect_to_socket()
    robot_detector= RobotDetector(communicator)
    try:
        robot_detector.run()

    finally:
        print("Close")
        communicator.close_connection()

def main1():
    communicator= Communicator(HOST_ADDR, TCP_PORT)
    communicator.connect_to_socket()
    try:
        #communicator.send_position(-105, 22, -22)
        #communicator.send_position(119, 22, -22)
        while True:
            pos= communicator.get_position()
            print(pos)
        print(communicator.get_position())
    finally:
        
        communicator.close_connection()
    
    
if __name__ == "__main__":
    main()


# -40 29 -20;
# TODO: Fixen, wenn er kein ack zurückbekommt, soll quit trotzdem die session killen