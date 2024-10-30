import cv2
from ultralytics import YOLO
import threading
import time
import pytesseract

model = YOLO('models/best.pt')

last_detection_time = time.time()

def detection_interval():
    current_time = time.time()
    if current_time - last_detection_time >= 0.5:
        return current_time, True
    return last_detection_time, False

def detection_thread(frame):
    results = model(frame)
    if results:
        for result in results:
            for det in result.boxes.data:
                x1, y1, x2, y2, conf, cls = det.tolist()

                if conf > 0.4:
                    print("Wykryto")
                    plate_img = frame[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite("detected.png", plate_img)

img = cv2.imread('car2.jpg', 1)
#img_resized = cv2.resize(img, (256, 192))


detection_thread_instance = threading.Thread(target=detection_thread, args=(img,))
detection_thread_instance.start()

