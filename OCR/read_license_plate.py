import pytesseract
import cv2
import easyocr
import time
#from preprocess import preprocess_img
from OCR.preprocess import preprocess_img
from paddleocr import PaddleOCR
import numpy as np

class ReadLicensePlate:
    def __init__(self):
        self.reader = PaddleOCR(use_angle_cls=True, use_gpu=False)

    def get_string(self, img):
        cv2.imwrite('detected_img.png', img)
        preprocessed_img = preprocess_img(img)
        if preprocessed_img is not None:
            img = preprocessed_img
            size_ratio = (preprocessed_img.shape[0]*preprocessed_img.shape[1])/(img.shape[0]*img.shape[1])
            if size_ratio > 0.65:
                img = preprocessed_img
        cv2.imwrite('preprocessed_img.png', img)

        result = self.reader.ocr(img, det=False, rec=True, cls=False)
        print(result)

        potential_license_plate = ""
        for r in result:
            scores = r[0][1]
            if np.isnan(scores):
                scores = 0
            else:
                scores = int(scores * 100)
            if scores > 80:
                potential_license_plate = r[0][0]

        if potential_license_plate:
            license_plate = self.filter_characters_pl(potential_license_plate)
            #print(license_plate)
            return license_plate
        else:
            return None


    def filter_characters_pl(self, text):
        allowed_characters = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"
        letters = "ABCDEFGHIJKLMNOPRSTUWXYZ"
        first_character = "BCDEFGKLNOPRSTWZU"
        text = text.upper()

        if len(text) > 4:
            middle_part = text[1:-1].replace('|', 'I').replace('!', 'I')
            text = text[0] + middle_part + text[-1]

            filtered_text = ''

            for char in text:
                if char in allowed_characters:
                    filtered_text += char

            if len(filtered_text) > 8:
                if (filtered_text[1] in first_character) and (filtered_text[2] in letters):
                    filtered_text = filtered_text[1:]

            if len(filtered_text) == 8:
                first_three = filtered_text[:3]
                replacements = {'1': 'I', '8': 'B', '6': 'G'}
                modified_first_three = ''.join(replacements.get(char, char) for char in first_three)
                filtered_text = modified_first_three + filtered_text[3:]

            if len(filtered_text) == 7:
                first_three = filtered_text[:2]
                replacements = {'1': 'I', '8': 'B', '6': 'G'}
                modified_first_three = ''.join(replacements.get(char, char) for char in first_three)
                filtered_text = modified_first_three + filtered_text[2:]

            if filtered_text[0] not in first_character:
                return None
        else:
            return None

        return filtered_text



if __name__ == '__main__':
    read_lp = ReadLicensePlate()
    img = cv2.imread('fiat1_pre.png', 1)
    print(read_lp.get_string(img))