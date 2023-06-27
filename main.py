import time
from gesture.communicator import Communicator
from gesture.detector import Detector

HOST_ADDR = "10.215.255.151"
TCP_PORT = 59002

HOME_POSITION = (48, -45, -22)
# MARGIN is necessary because the detection at the screen edge doesn't work well
MARGIN = 100

TARGET_Y_MIN = -115  # Minimum Y coordinate for target position
TARGET_Y_MAX = 119  # Maximum Y coordinate for target position
TARGET_Z_MIN = -44  # Minimum Z coordinate for target position
TARGET_Z_MAX = 51  # Maximum Z coordinate for target position


class RobotDetector(Detector):
    """
    Detector class for the robot's gestures.
    """

    def __init__(self, communicator):
        """
        Initialize the RobotDetector.

        Args:
            communicator (Communicator): 
                The communicator object used for communication with the robot.
        """
        super().__init__()
        self.communicator = communicator

    def one_index_finger_up(self, hand):
        """
        Handle the case when one index finger is raised.

        Args:
            hand (dict): A dictionary containing hand information.
        """
        lmList = hand["lmList"]
        index_finger_x = lmList[8][0]
        index_finger_y = lmList[8][1]

        # X coord image (==y on target)
        normalized_x = (index_finger_x - MARGIN) / (self.width - 2 * MARGIN)
        mapped_x = int(min(TARGET_Y_MAX,
                           max(TARGET_Y_MIN, TARGET_Y_MIN
                               + (TARGET_Y_MAX - TARGET_Y_MIN) * normalized_x)
                           ))

        # y coord image (==z on target)
        normalized_y = (index_finger_y - MARGIN) / (self.height - 2 * MARGIN)
        mapped_y = int(min(TARGET_Z_MAX,
                           max(TARGET_Z_MIN, TARGET_Z_MIN
                               + (TARGET_Z_MAX - TARGET_Z_MIN) * normalized_y)))

        # Fixed z Value: no depth detection activated
        z_Value = -22
        print(f"x: {mapped_x}, y: {z_Value} z: {mapped_y}")
        self.communicator.send_position(mapped_x, z_Value, mapped_y)
        time.sleep(0.05)

    def two_index_fingers_up(self, hand1, hand2):
        """
        Handle the case when two index fingers are raised.

        Args:
            hand1 (dict): 
                A dictionary containing information about the first hand.
            hand2 (dict): 
                A dictionary containing information about the second hand.
        """
        print("both_up")

    def two_all_fingers_down(self, hand1, hand2):
        """
        Handle the case when all fingers of both hands are down.

        Args:
            hand1 (dict): 
                A dictionary containing information about the first hand.
            hand2 (dict): 
                A dictionary containing information about the second hand.
        """
        print("Go to home position")
        self.communicator.send_position(*HOME_POSITION)
        position = self.communicator.get_position()

        print(position)
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < 10:
            coords = self.communicator.get_position().decode().split("|")
            rec_pos = tuple(float(coord) for coord in coords)
            if self._compare_positions(HOME_POSITION, rec_pos, 0.1):
                print("Positions match")
                break
            elapsed_time = time.time() - start_time

    def _compare_positions(self, sent_pos, rec_pos, threshold):
        """
        Compare the sent and received positions within a threshold.

        Args:
            sent_pos (tuple): The position coordinates sent to the robot.
            rec_pos (tuple): The position coordinates received from the robot.
            threshold (float): The threshold for position comparison.

        Returns:
            bool: 
                True if the positions are within the threshold, False otherwise.
        """
        for i in range(3):
            if abs(sent_pos[i] - rec_pos[i]) > threshold:
                return False
        return True


def main():
    """
    The main function that sets up the communication 
    and runs the robot detector.
    """
    communicator = Communicator(HOST_ADDR, TCP_PORT)
    communicator.connect_to_socket()
    robot_detector = RobotDetector(communicator)
    try:
        robot_detector.run()

    finally:
        print("Close")
        communicator.close_connection()


if __name__ == "__main__":
    main()
