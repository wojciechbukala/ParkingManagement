import cv2
import numpy
import socket
import struct

class StreamVideo:
    def __init__(self, client_ip='0.0.0.0', host_port=9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.max_packet_size = 20000
        self.client_ip = client_ip
        self.host_port = host_port 

    def stream_frame(self, frame):
        #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        img_bytes = imgencode.tobytes()
        self.server.sendto(struct.pack('i', len(img_bytes)), (self.client_ip, self.host_port))
        
        for i in range(0, len(img_bytes), self.max_packet_size):
            self.server.sendto(img_bytes[i:i+self.max_packet_size], (self.client_ip, self.host_port))
            

    def stop_streaming(self):
        self.server.close()

