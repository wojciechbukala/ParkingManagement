import socket
import struct
import threading
import time
import json

class SendData:
    def __init__(self, host_ip='0.0.0.0', host_port=9997):
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

    def send_data(self, data):
        json_data = json.dumps(data)
        json_data_encoded = json_data.encode('utf-8')

        message = struct.pack("Q", len(json_data_encoded)) + json_data_encoded

        for client in self.clients:
            try:
                client.sendall(message)
                print("[INFO] Dane tekstowe wysłane.")
            except (socket.error, OSError):
                print("[ERROR] Blad wysylania do klienta. Usuwam klienta")
                self.clients.remove(client)

    def stop_sending(self):
        self.connecting_clients_flag = False
        self.connecting_thread.join()
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    sender = SendData(host_ip='0.0.0.0', host_port=9997)

    data = {
        "plate_number": "DW123456",
        "add_to_db": "yes",
        "current_number_of_cars": 290
    }

    while True:
        sender.send_data(data)  # Wyślij danr
        time.sleep(10)