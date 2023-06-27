import socket
import time

BUFFER_SIZE = 1024


class Communicator:
    """
    A class for communicating with a socket server.
    """

    def __init__(self, host_addr: str, tcp_port: int):
        """
        Initialize the Communicator object.

        Args:
            host_addr (str): The IP address or hostname of the server.
            tcp_port (int): The TCP port number to connect to.
        """
        self.host_addr = host_addr
        self.tcp_port = tcp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_socket(self, retry_count=15):
        """
        Connect to the socket server.

        Args:
            retry_count (int): The number of connection retries.

        Raises:
            Exception: 
                If the connection is refused after the specified 
                number of retries.
        """
        counter = 0
        while True:
            try:
                print("Connecting...")
                addr = (self.host_addr, self.tcp_port)
                self.sock.connect(addr)
                return
            except ConnectionRefusedError as e:
                counter += 1
                if counter >= retry_count:
                    raise Exception(e) from e
                time.sleep(1)

    def send_data(self, data: str, timeout=2):
        """
        Send data to the server and receive the response.

        Args:
            data (str): The data to be sent to the server.
            timeout (int): The timeout duration for sending and receiving data.

        Returns:
            bytes:
                The response received from the server, 
                or None if an error occurred.
        """
        # Set a timeout of 2 seconds
        self.sock.settimeout(timeout)
        try:
            self.sock.send(data.encode())
            response = self.sock.recv(BUFFER_SIZE)
            return response
        except socket.timeout:
            print("Timeout while sending data.")
        except socket.error as e:
            print("Error while sending data:", e)
        return None

    def close_connection(self):
        """
        Close the connection to the server.
        """
        val = self.send_data("exit")
        print("Connection closed. Received:", val)
        self.sock.close()

    def send_position(self, x: float, y: float, z: float, decimal_place=3):
        """
        Send the position coordinates to the server.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            z (float): The z-coordinate.
            decimal_place (int): 
                The number of decimal places to round the coordinates.

        Returns:
            bytes: The response received from the server.
        """
        x_coord = round(x, decimal_place)
        y_coord = round(y, decimal_place)
        z_coord = round(z, decimal_place)
        data = self.send_data("set_pos")
        data = self.send_data(f"{x_coord} {y_coord} {z_coord};")
        return data

    def get_position(self):
        """
        Get the current position from the server.

        Returns:
            bytes: The response received from the server.
        """
        return self.send_data("get_pos")
