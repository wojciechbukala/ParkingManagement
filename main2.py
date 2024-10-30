from picamera2 import Picamera2
import cv2
from ultralytics import YOLO
import threading
import time
import json
from communication.stream_video import StreamVideo
from communication.send_img import SendImg
from OCR.read_license_plate import ReadLicensePlate
from communication.send_data import SendData
import database.settings as st
from database.db_selects import Selects

class LicensePlateRecognition:
    def __init__(self):
        self.init_settings()
        self.init_models()
        self.init_communication()

        #Camera setup
        self.cam = self.cam_setup()

        #Last detection time
        self.last_detection_time = time.time()

    def init_settings(self):
        st.load_settings()
        self.settings = st.settings

    def init_models(self):
        self.recognition_model = YOLO(f'models/{st.settings["recognition_model"]}')
        self.OCR_model = ReadLicensePlate()

    def init_communication(self):
        self.stream_video = StreamVideo('192.168.1.125', 9999)
        self.selects = Selects()

    def cam_setup(self):
        cam = Picamera2()
        cam.preview_configuration.main.format = "RGB888"
        cam.preview_configuration.align()
        cam.configure("preview")
        cam.start()
        return cam

    def detection_interval():
        current_time = time.time()
        if current_time - self.last_detection_time >= 3:
            self.last_detection_time = current_time
            return True
        return False

    def detect_license_plate(self, frame):
        results = self.recognition_model(frame)

        if results:
            for results in results:
                for det in results.boxes.data:
                    x1, y1, x2, y2, conf, cls = det.tolist()

                    if conf > st.settings["recognition_confidence"]:
                        plate_img = frame[int(y1):int(y2), int(x1):int(x2)]
                        cv2.imwrite("database/detected.png", plate_img)
                        license_plate = OCR_model.get_string(plate_img)

                        handle_detection_thread = threading.Thread(target=handle_detection, args=(license_plate, conf))
                        handle_detection_thread .start()

    def handle_detection(self, license_plate, confidence):
        if st.settings["mode"] == "authorized":
            acceptance = selects.check_authorization(license_plate)
        else:
            acceptance = True

        data = {
            "license_plate": license_plate,
            "acceptance": acceptance,
            "confidence": confidence,
            "model": st.settings["recognition_model"]
        }
        with open("database/detection_data.json", 'w') as f:
            json.dump(data, f, indent=4)

    def run(self):
        while True:
            img = self.cam.capture_array()

            if self.detection_interval():
                detection_thread_instance = threading.Thread(target=self.detect_license_plate, args=(img,))
                detection_thread_instance.start()

            stream.stream_frame(img)

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        st.stop_streaming()

if __name__ == '__main__':
    system = LicensePlateRecognition()
    system
