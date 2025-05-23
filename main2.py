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
from database.db_inserts import Inserts
import gpio


pattern = 'ZPL80264'
total_recognitions = 0
total_detections = 0
good_detections = 0
good_recognitions = 0

gate_open = False


class LicensePlateRecognition:
    def __init__(self):
        self.init_settings()
        self.init_models()
        self.init_communication()

        #Camera setup
        self.cam = self.cam_setup()

        #Last detection time
        self.last_detection_time = time.time()

        self.init_gpio()

    def init_settings(self):
        st.load_settings()
        self.settings = st.settings

    def init_models(self):
        self.recognition_model = YOLO(f'models/{self.settings["recognition_model"]}')
        self.OCR_model = ReadLicensePlate()

    def init_communication(self):
        self.stream_video = StreamVideo(st.settings["client_ip"], 9999)
        self.selects = Selects()
        self.inserts = Inserts()
        self.detection_data = st.detection_data

    def init_gpio(self):
        self.gpio_handler = gpio.GPIO_Handler()
        with open("database/global_data.json", 'r') as f:
            global_vars = json.load(f)

        global_vars["gate_state"] = gpio.gate_open

        with open("database/global_data.json", 'w') as f:
            json.dump(global_vars, f, indent=4)

    def cam_setup(self):
        cam = Picamera2()
        cam.preview_configuration.main.format = "RGB888"
        cam.preview_configuration.align()
        cam.configure("preview")
        cam.start()
        return cam

    def settings_update(self):
        with open('database/settings.json', 'r') as f:
            settings = json.load(f)
            if settings.get("updated_flag"):
                self.init_settings()
                settings["updated_flag"] = False
                with open('database/settings.json', 'w') as file:
                    json.dump(settings, file, indent=4)
                self.stream_video = StreamVideo(st.settings["client_ip"], 9999)

    def detection_interval(self):
        current_time = time.time()
        if current_time - self.last_detection_time >= self.settings["detection_interval"]:
            self.last_detection_time = current_time
            return True
        return False

    def detect_license_plate(self, frame):
        results = self.recognition_model(frame)

        if results:
            for results in results:
                for det in results.boxes.data:
                    x1, y1, x2, y2, conf, cls = det.tolist()

                    if conf > self.settings["recognition_confidence"]:
                        plate_img = frame[int(y1):int(y2), int(x1):int(x2)]
                        cv2.imwrite("database/detected.png", plate_img)
                        license_plate = self.OCR_model.get_string(plate_img)

                        if license_plate is not None:
                            handle_detection_thread = threading.Thread(target=self.handle_detection, args=(license_plate, conf))
                            handle_detection_thread .start()

                            #test
                            global total_recognitions
                            global good_detections
                            total_recognitions += 1
                            good_detections += 1

    def handle_detection(self, license_plate, confidence):
        acceptance = True
        car_already_exists_error = False
        capacity_full_error = False
        data = {}

        #test
        global good_recognitions
        global pattern
        if license_plate == pattern:
            good_recognitions += 1

        if self.settings["mode"] == "authorized":
            acceptance = self.selects.check_authorization(license_plate)

        if acceptance:
            if self.selects.check_car_exist(license_plate):
                acceptance = False
                car_already_exists_error = True

            else:   

                if self.selects.currently_parked_cars() >= self.settings["total_capacity"]:
                    acceptance = False
                    capacity_full_error = True

                else:
                    self.inserts.insert_car(license_plate)
                  
        self.detection_data = {
            "license_plate": license_plate,
            "acceptance": acceptance,
            "confidence": confidence,
            "model": self.settings["recognition_model"],
            "capacity_occupied": data.get("currently_parked", 0),
            "already_exists": car_already_exists_error,
            "capacity_full": capacity_full_error
        }

        with open("database/detection_data.json", 'w') as f:
            json.dump(self.detection_data, f, indent=4)

        if acceptance == True:
            self.gpio_handler.handle_gpio_recognition()

    def run(self):
        while True:
            self.settings_update()

            img = self.cam.capture_array()

            self.gpio_handler.handle_gpio_inputs()

            if self.detection_interval() and not gpio.gate_open:
                detection_thread_instance = threading.Thread(target=self.detect_license_plate, args=(img,))
                detection_thread_instance.start()

                #test
                global total_recognitions
                global total_detections
                global good_recognitions
                global good_detections

                total_detections += 1

                print(f"TR: {total_recognitions}, TD: {total_detections}, GR: {good_recognitions}, GD: {good_detections} ")

            #cv2.imshow("Camera", img)
            self.stream_video.stream_frame(img)

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        st.stop_streaming()

if __name__ == '__main__':
    system = LicensePlateRecognition()
    system.run()
