import pytesseract
import cv2
import easyocr
import time
#from preprocess import preprocess_img
from OCR.preprocess import preprocess_img
from paddleocr import PaddleOCR
import numpy as np

class ReadLicensePlate:
    # def __init__(self):
    #     self.tesseract_config = r'--oem 3 --psm 7 tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789'

    # def get_string(self, img):
    #     preprocessed_img = preprocess_img(img)
    #     if preprocessed_img is not None:
    #         size_ratio = (preprocessed_img.shape[0]*preprocessed_img.shape[1])/(img.shape[0]*img.shape[1])
    #         if size_ratio > 0.65:
    #             img = preprocessed_img
    #     cv2.imwrite('preprocessed.png', img)
    #     potential_license_plate = pytesseract.image_to_string(img, lang='eng', config=self.tesseract_config)
    #     license_plate = self.filter_characters_pl(potential_license_plate)
    #     # if license_plate == None:
    #     #     license_plate = "Not detected"
    #     return license_plate

    # def __init__(self):
    #     self.reader = easyocr.Reader(['en'], gpu=False)

    # def get_string(self, img):
    #     cv2.imwrite('detected_img.png', img)
    #     preprocessed_img = preprocess_img(img)
    #     if preprocessed_img is not None:
    #         img = preprocessed_img
    #         # size_ratio = (preprocessed_img.shape[0]*preprocessed_img.shape[1])/(img.shape[0]*img.shape[1])
    #         # if size_ratio > 0.65:
    #         #     img = preprocessed_img
    #     cv2.imwrite('preprocessed_img.png', img)
    #     start_time = time.time()
    #     result = self.reader.readtext(img, detail=0)  # detail=0: tylko tekst
    #     end_time = time.time()

    #     potential_license_plate = ''
    #     for text in result:
    #         potential_license_plate += text

    #     if potential_license_plate:
    #         license_plate = self.filter_characters_pl(potential_license_plate)
    #         print(end_time - start_time)
    #         print(license_plate)
    #         return license_plate
    #     else:
    #         return None

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
        text = text.replace('|', 'I').replace('!', 'I')

        filtered_text = ''

        for char in text:
            if char in allowed_characters:
                filtered_text += char

        if len(filtered_text) > 8:
            if (filtered_text[1] in first_character) and (filtered_text[2] in letters) and (filtered_text[3] in letters):
                filtered_text = filtered_text[1:]
        elif len(filtered_text) < 4:
            return None

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

        return filtered_text



if __name__ == '__main__':
    read_lp = ReadLicensePlate()
    img = cv2.imread('fiat1_pre.png', 1)
    print(read_lp.get_string(img))