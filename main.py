import socket
import time

HOST_ADDR="10.215.255.151"
TCP_PORT=59002
BUFFER_SIZE = 1024

def connect_socket(retry_count):
    """
    Args:
        retry_count (int): Anzahl retrys connection
    """
    counter=0
    while True:
        try:
            print("Connecting...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = (HOST_ADDR, TCP_PORT)
            sock.connect(addr)
            return sock
        except ConnectionRefusedError as e:
            counter +=1
            if counter >= retry_count:
                raise Exception(e) from e
            time.sleep(1)

def main():
    sock = connect_socket(10)

    try:
        running=True
        counter=0
        startwert= int(-104)
        while running:
            print("Eingabe Bitte")
            print("Enter Cords or exit for disconnect:")
            eingabe = input()
            if eingabe == "exit" or eingabe == "shutdown_server":
                print("Disconnecting...")
                running=False
            else:
                counter += 1
                print(counter)
                sock.send("set_pos".encode())
                data = sock.recv(BUFFER_SIZE)
                send_msg=f"{startwert} 22 -22;"
                sock.send(send_msg.encode())
                data = sock.recv(BUFFER_SIZE)
                print(data.decode())
                if startwert < 130:
                    startwert +=10
                else:
                    startwert=-105
                

    finally:
        sock.send("exit".encode())
        data = sock.recv(BUFFER_SIZE)
        sock.close()
    
    
if __name__ == "__main__":
    main()

# -40 29 -20;
