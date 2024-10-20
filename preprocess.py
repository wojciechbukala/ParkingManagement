import pytesseract
import cv2
import numpy as np
from detect_edges import detect_edges

class ReadLicensePlate:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZQ0123456789'

    def img_preprocess(self, img):
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # #img = cv2.GaussianBlur(img, (5,5), 0)
        # # Step 1: Sharpen the image using a sharpening kernel
        # sharpen_kernel = np.array([[-1, -1, -1],
        #                    [-1,  3, -1],
        #                    [-1, -1, -1]])

        # # Apply the kernel to the image
        # img = cv2.filter2D(img, -1, sharpen_kernel)


        edges = cv2.Canny(img, 30, 60)

        lines = cv2.HoughLinesPlines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
        cv2.imwrite('preprocessed2.png', img)
        return img

    def get_string(self, img):
        img = self.img_preprocess(img)
        potential_license_plate = pytesseract.image_to_string(img, lang='eng', config=self.tesseract_config)
        print(potential_license_plate)

img2 = cv2.imread('preprocessed.png', 1)
rlp = ReadLicensePlate()
rlp.get_string(img2)