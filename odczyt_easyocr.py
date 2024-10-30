import cv2
import easyocr
import time

# Wczytanie obrazu i wstępne przetwarzanie dla optymalizacji
img = cv2.imread('preprocessed.png', cv2.IMREAD_GRAYSCALE)  # Konwersja do skali szarości
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)  # Zmniejszenie rozmiaru obrazu
_, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)  # Binaryzacja (czarno-biały obraz)

# Inicjalizacja EasyOCR z ustawieniami dla pojedynczego języka i bez GPU
reader = easyocr.Reader(['en'], gpu=False)

# Pomiar czasu przetwarzania tekstu
start_time = time.time()
cv2.imwrite("preprocessed2.png", img)
result = reader.readtext(img, detail=0)  # detail=0: zwraca tylko tekst bez ramki
end_time = time.time()

# Wyświetlenie wykrytego tekstu
for text in result:
    print(f'Text: {text}')

# Wyświetlenie czasu przetwarzania
processing_time = end_time - start_time
print(f'Time taken for text detection: {processing_time:.4f} seconds')
