import pytesseract
import cv2
import easyocr
import time
#from preprocess import preprocess_img
from OCR.preprocess import preprocess_img

class ReadLicensePlate:
    # def __init__(self):
    #     self.tesseract_config = r'--oem 3 --psm 7 tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789'

    #     def get_string(self, img):
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

    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def get_string(self, img):
        preprocessed_img = preprocess_img(img)
        if preprocessed_img is not None:
            size_ratio = (preprocessed_img.shape[0]*preprocessed_img.shape[1])/(img.shape[0]*img.shape[1])
            if size_ratio > 0.65:
                img = preprocessed_img
        start_time = time.time()
        result = self.reader.readtext(img, detail=0)  # detail=0: tylko tekst
        end_time = time.time()

        potential_license_plate = ''
        for text in result:
            potential_license_plate += text

        if potential_license_plate:
            license_plate = self.filter_characters_pl(potential_license_plate)
            print(end_time - start_time)
            return license_plate
        else:
            return None


    def filter_characters_pl(self, text):
        allowed_characters = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"
        letters = "ABCDEFGHIJKLMNOPRSTUWXYZ"
        first_character = "BCDEFGKLNOPRSTWZU"

        filtered_text = ''

        for char in text:
            if char in allowed_characters:
                filtered_text += char

        if len(filtered_text) > 8:
            if (filtered_text[1] in first_character) and (filtered_text[2] in letters) and (filtered_text[3] in letters):
                filtered_text = filtered_text[1:]
        elif len(filtered_text) < 4:
            return None
        
        if filtered_text[0] not in first_character:
            return None

        return filtered_text



if __name__ == '__main__':
    read_lp = ReadLicensePlate()
    img = cv2.imread('fiat2_pre.png', 1)
    print(read_lp.get_string(img))