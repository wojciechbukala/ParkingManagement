import cv2
import numpy as np
# from detect_blue import cut_blue_region
# from detect_edges import detect_edges
from OCR.detect_blue import cut_blue_region
from OCR.detect_edges import detect_edges

def preprocess_img(img):
    img_color = cut_blue_region(img)
    
    if img_color is None:
        img_color = img
    
    gray_img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    edges = detect_edges(gray_img)
    print(edges)

    right_edge = edges.get('right_edge', None)
    top_edge = edges.get('top_edge', None)
    bottom_edge = edges.get('bottom_edge', None)

    if right_edge is not None:
        max_x = max(right_edge[0], right_edge[2])
        img_color = img_color[:, :max_x]

    if top_edge is not None:
        min_y = min(top_edge[1], top_edge[3])
        img_color = img_color[min_y:, :]

    if bottom_edge is not None:
        max_y = max(bottom_edge[1], bottom_edge[3])
        img_color = img_color[:max_y, :]


    cv2.imwrite('preprocessed.png', img_color)
    return img_color


if __name__ == '__main__':
    image = cv2.imread('merc6_pre.png')
    print(image.shape)

    preprocess_img(image)

