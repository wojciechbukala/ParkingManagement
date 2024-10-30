import cv2
import numpy as np

def sharpen_image(image):
    sharpening_kernel = np.array([[0, -1, 0],
                                  [-1, 5, -1],
                                  [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
    return sharpened_image

def detect_edges(image):
    sharpened_image = sharpen_image(image)
    edges = {'right_edge': None, 'top_edge': None, 'bottom_edge': None}
    canny_img = cv2.Canny(sharpened_image, 20, 100)

    ver_line_len = int(0.15 * image.shape[0])
    ver_thresh = int(0.1 * image.shape[0])
    ver_gap = int(0.3 * image.shape[0])

    hor_line_len = int(0.15 * image.shape[1])
    hor_thresh = int(0.1 * image.shape[1])
    hor_gap = int(0.3 * image.shape[1])

    ver_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=ver_thresh, minLineLength=ver_line_len, maxLineGap=ver_gap)
    hor_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=hor_thresh, minLineLength=hor_line_len, maxLineGap=hor_gap)

    right_edge_lines = []
    top_edge_lines = []
    bottom_edge_lines = []

    right_edge_range = (int(0.95 * image.shape[1]), int(0.98 * image.shape[1]))
    top_edge_range = (int(0.02 * image.shape[0]), int(0.10 * image.shape[0]))
    bottom_edge_range = (int(0.90 * image.shape[0]), int(0.98 * image.shape[0]))

    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

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
                if top_edge_range[0] <= y1 <= top_edge_range[1]:
                    top_edge_lines.append((x1, y1, x2, y2))
                if bottom_edge_range[0] <= y1 <= bottom_edge_range[1]:
                    bottom_edge_lines.append((x1, y1, x2, y2))

    right_edge = max(right_edge_lines, key=lambda edge: edge[0]) if right_edge_lines else None
    top_edge = min(top_edge_lines, key=lambda edge: edge[1]) if top_edge_lines else None
    bottom_edge = max(bottom_edge_lines, key=lambda edge: edge[1]) if bottom_edge_lines else None

    edges['right_edge'] = right_edge
    edges['top_edge'] = top_edge
    edges['bottom_edge'] = bottom_edge

    # # Draw the detected lines on the output image
    # line_color = (0, 255, 0)  # Green
    # line_thickness = 2

    # for edge in [right_edge, top_edge, bottom_edge]:
    #     if edge is not None:
    #         x1, y1, x2, y2 = edge
    #         cv2.line(output_image, (x1, y1), (x2, y2), line_color, line_thickness)

    # # Display the images with detected edges
    # cv2.imshow("Sharpened Image", sharpened_image)
    # cv2.imshow("Detected Lines", output_image)
    # cv2.imshow("Canny Edges", canny_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return edges

if __name__ == '__main__':
    # Load the image in grayscale mode
    image = cv2.imread('license3.png', cv2.IMREAD_GRAYSCALE)

    # Call the function
    print(detect_edges(image))
