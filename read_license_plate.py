import pytesseract
import cv2

class ReadLicensePlate:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6 tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789'

    def img_preprocess(self, img):
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('preprocessed.png', img)
        return img

    def get_string(self, img):
        img = self.img_preprocess(img)
        potential_license_plate = pytesseract.image_to_string(img, lang='eng', config=self.tesseract_config)
        #check_license_plate
        print(potential_license_plate)
        return potential_license_plate
