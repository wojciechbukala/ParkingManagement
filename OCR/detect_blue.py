import cv2
import numpy as np

def detect_blue_areas(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_blue = np.array([105, 200, 70])
    upper_blue = np.array([130, 255, 255]) 
    
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    blue_areas = cv2.bitwise_and(image, image, mask=blue_mask)
    
    return blue_mask, blue_areas

def cut_blue_region(image):
    blue_mask, _ = detect_blue_areas(image)
    
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        image = image[:, w+int(image.shape[1]*0.015):]
        
        # # Wyświetl wykryty obszar niebieski
        # cv2.imshow("Detected Blue Area", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return image
    else:
        return None

if __name__ == '__main__':
    # Wczytaj obraz tablicy rejestracyjnej
    image = cv2.imread('license2.png')  # Zastąp 'european_license_plate.png' ścieżką do swojego obrazu

    # Wytnij i pokaż niebieski obszar tablicy rejestracyjnej
    extracted_region = extract_blue_region(image)