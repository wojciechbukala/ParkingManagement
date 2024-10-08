from picamera2 import Picamera2
import cv2
from stream_video import Stream

def cam_setup():
    cam = Picamera2()
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()

    return cam

frame = cam_setup()
st = Stream('192.168.1.125', 9999)

while True:
    img = frame.capture_array()
    cv2.imshow("Camera", img)

    st.stream_frame(img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
st.stop_streaming()
