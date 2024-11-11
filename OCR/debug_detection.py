import cv2
import numpy as np

def sharpen_image(image):
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
    return sharpened_image

image = cv2.imread('blue_area.png')
output_img = image
o_img = image.copy()

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sharpened_image = sharpen_image(gray_img)

canny_img = cv2.Canny(sharpened_image, 20, 100)

hor_line_len = int(0.45 * image.shape[1])
hor_thresh = int(0.08 * image.shape[1])
hor_gap = int(0.2 * image.shape[1])

ver_line_len = int(0.25 * image.shape[0])
ver_thresh = int(0.06 * image.shape[0])
ver_gap = int(0.25 * image.shape[0])



ver_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=ver_thresh, minLineLength=ver_line_len, maxLineGap=ver_gap)


hor_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=hor_thresh, minLineLength=hor_line_len, maxLineGap=hor_gap)


top_edge_lines = []
top_edge_range = (int(0.04 * image.shape[0]), int(0.20 * image.shape[0]))
bottom_edge_lines = []
bottom_edge_range = (int(0.85 * image.shape[0]), int(0.97 * image.shape[0]))
right_edge_lines = []
right_edge_range = (int(0.95 * image.shape[1]), int(0.98 * image.shape[1]))

if ver_lines is not None:
    for line in ver_lines:
        x1, y1, x2, y2 = line[0]
        angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)

        if 88 < angle < 92:
            if right_edge_range[0] <= x1 <= right_edge_range[1]:
                right_edge_lines.append((x1, y1, x2, y2))

if hor_lines is not None:
    for line in hor_lines:
        x1, y1, x2, y2 = line[0]
        angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)

        if 0 < angle < 2.5 or 177.5 < angle < 180:
            #cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            if top_edge_range[0] <= y1 <= top_edge_range[1]:
                top_edge_lines.append((x1, y1, x2, y2))
                #cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            if bottom_edge_range[0] <= y1 <= bottom_edge_range[1]:
                bottom_edge_lines.append((x1, y1, x2, y2))
                #cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 1)  # Zielone linie, grubość 2 piksele

# left_edge = min(left_edge_lines, key=lambda edge: edge[0]) if left_edge_lines else None
right_edge = max(right_edge_lines, key=lambda edge: edge[0]) if right_edge_lines else None
top_edge = min(top_edge_lines, key=lambda edge: edge[1]) if top_edge_lines else None
bottom_edge = max(bottom_edge_lines, key=lambda edge: edge[1]) if bottom_edge_lines else None


if top_edge is not None:
    cv2.line(output_img, (top_edge[0], top_edge[1]), (top_edge[2], top_edge[3]), (0, 0, 255), 1)  # Zielone linie, grubość 2 piksele
if bottom_edge is not None:
    cv2.line(output_img, (bottom_edge[0], bottom_edge[1]), (bottom_edge[2], bottom_edge[3]), (0, 0, 255), 1)

if right_edge is not None:
    cv2.line(output_img, (right_edge[0], right_edge[1]), (right_edge[2], right_edge[3]), (0, 0, 255), 1)



if right_edge is not None:
    max_x = max(right_edge[0], right_edge[2])
    o_img = o_img[:, :max_x]

if top_edge is not None:
    min_y = min(top_edge[1], top_edge[3])
    o_img = o_img[min_y:, :]

if bottom_edge is not None:
    max_y = max(bottom_edge[1], bottom_edge[3])
    o_img = o_img[:max_y, :]

#Zapisanie i wyświetlenie obrazu z wykrytymi liniami
cv2.imwrite('canny.png', canny_img)
cv2.imwrite('output_with_lines.jpg', output_img)
cv2.imwrite('output_final.png', o_img)
