import socket
import pickle
import pickle
import struct
import threading

class Stream:
    def __init__(self, host_ip='0.0.0.0', host_port=10050):
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
        
    def stream_frame(self, frame):
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        for client in self.clients:
            try:
                client.sendall(message)
            except (socket.error, OSError):
                self.clients.remove(client)

    def stop_streaming(self):
        self.connecting_clients_flag = False
        self.connecting_thread.join()
        for client in self.clients:
            client.close()
        self.server_socket.close()
