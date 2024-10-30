import pytesseract
import cv2
#from preprocess import preprocess_img
from OCR.preprocess import preprocess_img

class ReadLicensePlate:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6 tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789'

    def get_string(self, img):
        img = preprocess_img(img)
        cv2.imwrite('preprocessed.png', img)
        potential_license_plate = pytesseract.image_to_string(img, lang='eng', config=self.tesseract_config)
        print(potential_license_plate)
        return potential_license_plate

if __name__ == '__main__':
    read_lp = ReadLicensePlate()
    img = cv2.imread('license3.png', 1)
    read_lp.get_string(img)