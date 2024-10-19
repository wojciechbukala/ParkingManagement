import cv2
import socket
import struct
import threading
import pickle
import time

class SendImg:
    def __init__(self, host_ip='0.0.0.0', host_port=9998):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = host_ip
        self.host_port = host_port 
        self.server_socket.bind((self.host_ip, self.host_port))
        self.server_socket.listen(3)

        self.clients = []
        self.connecting_clients_flag = True
        self.connecting_thread = threading.Thread(target=self.conn_clients)
        self.connecting_thread.start()

    def conn_clients(self):
        while self.connecting_clients_flag:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"[INFO] Połączono z {address}")

    def send_frame(self, frame):
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        print("Szukam klientow")
        for client in self.clients:
            try:
                client.sendall(message)
                print("[INFO] Obraz wysłany.")
            except (socket.error, OSError):
                print("[ERROR] Błąd wysyłania do klienta. Usuwam klienta.")
                self.clients.remove(client)

    def stop_sending(self):
        self.connecting_clients_flag = False
        self.connecting_thread.join()
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    sender = Send_License_Plate(host_ip='0.0.0.0', host_port=9998)

    img = cv2.imread("Cars389.png")  # Załaduj obraz

    while True:
        sender.send_frame(img)  # Wyślij obraz
        time.sleep(2)
        

