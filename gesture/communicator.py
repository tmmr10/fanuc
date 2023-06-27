import socket
import time

BUFFER_SIZE = 1024


class Communicator:

    def __init__(self, host_addr: str, tcp_port: int):
        self.host_addr = host_addr
        self.tcp_port = tcp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_socket(self, retry_count=15):
        """
        Args:
            retry_count (int): Anzahl retrys connection
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
        # Setze einen Timeout von 5 Sekunden
        self.sock.settimeout(timeout)
        try:
            self.sock.send(data.encode())
            response = self.sock.recv(BUFFER_SIZE)
            return response
        except socket.timeout:
            print("Timeout beim Senden von Daten.")
        except socket.error as e:
            print("Fehler beim Senden von Daten:", e)
        return None

    def close_connection(self):
        val = self.send_data("exit")
        print("Closed Connection. Recieved: ", val)
        self.sock.close()

    def send_position(self, x: float, y: float, z: float, decimal_place=3):
        x_coord = round(x, decimal_place)
        y_coord = round(y, decimal_place)
        z_coord = round(z, decimal_place)
        data = self.send_data("set_pos")
        data = self.send_data(f"{x_coord} {y_coord} {z_coord};")
        return data

    def get_position(self):
        return self.send_data("get_pos")
