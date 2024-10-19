from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import threading
import time
from communication.stream_video import StreamVideo
from communication.send_img import SendImg
from read_license_plate import ReadLicensePlate
from communication.send_data import SendData

recognition_model = YOLO('models/best.pt')

last_detection_time = time.time()

OCR_model = ReadLicensePlate()

sender_img = SendImg(host_ip='0.0.0.0', host_port=9998)
sender_data = SendData(host_ip='0.0.0.0', host_port=9997)

def detection_interval():
    current_time = time.time()
    if current_time - last_detection_time >= 3:
        return current_time, True
    return last_detection_time, False

def detection_thread(frame):
    results = recognition_model(frame)
    if results:
        for result in results:
            for det in result.boxes.data:
                x1, y1, x2, y2, conf, cls = det.tolist()

                if conf > 0.2:
                    plate_img = frame[int(y1):int(y2), int(x1):int(x2)]
                    sender_img.send_frame(plate_img)
                    license_plate = OCR_model.get_string(plate_img)
                    data = {
                        "license_plate": license_plate
                    }
                    sender_data.send_data(data)


def cam_setup():
    cam = Picamera2()
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()

    return cam

frame = cam_setup()
st = StreamVideo('192.168.1.125', 9999)

while True:
    img = frame.capture_array()

    last_detection_time, interval = detection_interval()
    if interval == True:
        detection_thread_instance = threading.Thread(target=detection_thread, args=(img,))
        detection_thread_instance.start()

    cv2.imshow("Camera", img)
    st.stream_frame(img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
st.stop_streaming()