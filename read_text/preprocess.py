import pytesseract
import cv2
import numpy as np
from detect_edges import detect_edges

class ReadLicensePlate:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZQ0123456789'

    def img_preprocess(self, img):
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = detect_edges(img)
        print(edges)

        left_edge = edges.get('left_edge', None)
        right_edge = edges.get('right_edge', None)
        top_edge = edges.get('top_edge', None)
        bottom_edge = edges.get('bottom_edge', None)

        if left_edge is not None:
            img = img[:, min(left_edge[0], left_edge[2]):]

            if left_edge[2] != left_edge[0]:
                x1 = left_edge[0] - min(left_edge[0], left_edge[2])
                x2 = left_edge[2] - min(left_edge[0], left_edge[2])
                a = (left_edge[3] - left_edge[1]) / (x2 - x1)
                b = (-1)* a * left_edge[0]

                for y in range(img.shape[0]-1):
                    for x in range(img.shape[1] // 8):
                        if x < ((y-b)/a):
                            img[y, x] = 0


        if right_edge is not None:
            img = img[:, :max(right_edge[0], right_edge[2])]

            if right_edge[2] != right_edge[0]:
                a = (right_edge[3] - right_edge[1]) / (right_edge[2] - right_edge[0])
                b = (-1)* a * right_edge[0]

                for y in range(img.shape[0]-1):
                    for x in range((4*img.shape[1]) // 5, img.shape[1]-1):
                        if x > ((y-b)/a):
                            img[y, x] = 0

        if top_edge is not None:
            img = img[min(top_edge[1], top_edge[3]):, :]

            if top_edge[3] != top_edge[1]:
                y1 = top_edge[1] - min(top_edge[1], top_edge[3])
                y2 = top_edge[3] - min(top_edge[1], top_edge[3])
                a = (y2 - y1) / (top_edge[2] - top_edge[0])
                b = top_edge[1]

                for x in range(img.shape[1]-1):
                    for y in range(img.shape[0] // 5):
                        if y < ((a*x)+b):
                            img[y, x] = 0


        if bottom_edge is not None:     
            img = img[:max(bottom_edge[1], bottom_edge[3]), :]

            if bottom_edge[3] != bottom_edge[1]:
                a = (bottom_edge[3] - bottom_edge[1]) / (bottom_edge[2] - bottom_edge[0])
                b = bottom_edge[1]

                for x in range(img.shape[1]-1):
                    for y in range((3*img.shape[0]) // 4, img.shape[0]-1):
                        if y > ((a*x)+b):
                            img[y, x] = 0



        cv2.imwrite('preprocessed2.png', img)
        return img

    def get_string(self, img):
        img = self.img_preprocess(img)
        potential_license_plate = pytesseract.image_to_string(img, lang='eng', config=self.tesseract_config)
        print(potential_license_plate)

img2 = cv2.imread('detected.png', 1)
rlp = ReadLicensePlate()
rlp.get_string(img2)