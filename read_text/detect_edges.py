import cv2
import numpy as np

def detect_edges(image):
    edges = {'left_edge' : None, 'right_edge' : None,
            'top_edge' : None, 'bottom_edge': None}

    canny_img = cv2.Canny(image, 20, 100)

    ver_line_len = int(0.35 * image.shape[0])
    ver_thresh = int(0.1 * image.shape[0])
    ver_gap = int(0.05 * image.shape[0])

    hor_line_len = int(0.2 * image.shape[1])
    hor_thresh = int(0.15 * image.shape[1])
    hor_gap = int(0.1 * image.shape[1])

    ver_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=ver_thresh, minLineLength=ver_line_len, maxLineGap=ver_gap)
    hor_lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, threshold=hor_thresh, minLineLength=hor_line_len, maxLineGap=hor_gap)

    left_edge_lines = []
    right_edge_lines = []
    top_edge_lines = []
    bottom_edge_lines = []

    left_edge_range = (int(0.04 * image.shape[1]), int(0.14 * image.shape[1]))
    right_edge_range = (int(0.95 * image.shape[1]), int(0.98 * image.shape[1]))
    top_edge_range = (int(0.02 * image.shape[0]), int(0.14 * image.shape[0]))
    bottom_edge_range = (int(0.8 * image.shape[0]), int(0.98 * image.shape[0]))

    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    if ver_lines is not None:
        for line in ver_lines:
            x1, y1, x2, y2 = line[0]
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)  # Calculate the angle of the line

            if 85 < angle < 95:
                if left_edge_range[0] <= x1 <= left_edge_range[1]:
                    left_edge_lines.append((x1, y1, x2, y2))
                if right_edge_range[0] <= x1 <= right_edge_range[1]:
                    right_edge_lines.append((x1, y1, x2, y2))

    if left_edge_lines:
        left_edge = min(left_edge_lines, key=lambda edge: edge[0])
        x1, y1, x2, y2 = left_edge

        a = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        y1_streched = 0
        y2_streched = image.shape[0]

        x1_streched = int(x1 + (y1_streched - y1) / a) if a != 0 else x1
        if x1_streched < 0:
            x1_streched = 0
        x2_streched = int(x2 + (y2_streched - y1) / a) if a != 0 else x2
        if x2_streched < 0:
            x2_streched = 0

        cv2.line(output_image, (x1_streched, y1_streched), (x2_streched, y2_streched), (255, 0, 0), 2)
        edges['left_edge'] = (x1_streched, y1_streched, x2_streched, y2_streched)

    if right_edge_lines:
        right_edge = max(right_edge_lines, key=lambda edge: edge[0])
        x1, y1, x2, y2 = right_edge

        a = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        y1_streched = 0
        y2_streched = image.shape[0]

        x1_streched = int(x1 + (y1_streched - y1) / a) if a != 0 else x1
        if x1_streched < 0:
            x1_streched = 0
        x2_streched = int(x2 + (y2_streched - y1) / a) if a != 0 else x2
        if x2_streched < 0:
            x2_streched = 0

        cv2.line(output_image, (x1_streched, y1_streched), (x2_streched, y2_streched), (255, 0, 0), 2)
        edges['right_edge'] = (x1_streched, y1_streched, x2_streched, y2_streched)

    if hor_lines is not None:
        for line in hor_lines:
            x1, y1, x2, y2 = line[0]
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)

            if 0 < angle < 2.5 or 177.5 < angle < 180:
                if top_edge_range[0] <= y1 <= top_edge_range[1]:
                    top_edge_lines.append((x1, y1, x2, y2))
                if bottom_edge_range[0] <= y1 <= bottom_edge_range[1]:
                    bottom_edge_lines.append((x1, y1, x2, y2))

    if top_edge_lines:
        top_edge = min(top_edge_lines, key=lambda edge: edge[1])
        x1, y1, x2, y2 = top_edge

        a = (y2 - y1) / (x2 - x1) if y2 != y1 else 0
        x1_streched = 0
        x2_streched = image.shape[1]

        y1_streched = int(y1 + (x1_streched - x1) * a) if a != 0 else y1
        if y1_streched < 0:
            y1_streched = 0
        y2_streched = int(y2 + (x2_streched - x1) * a) if a != 0 else y2
        if y2_streched < 0:
            y2_streched = 0

        cv2.line(output_image, (x1_streched, y1_streched), (x2_streched, y2_streched), (255, 0, 0), 2)
        edges['top_edge'] = (x1_streched, y1_streched, x2_streched, y2_streched)

    if bottom_edge_lines:
        bottom_edge = max(bottom_edge_lines, key=lambda edge: edge[1])
        x1, y1, x2, y2 = bottom_edge

        a = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        x1_streched = 0
        x2_streched = image.shape[1]

        y1_streched = int(y1 + (x1_streched - x1) * a) if a != 0 else x1
        if y1_streched < 0:
            y1_streched = 0
        y2_streched = int(y2 + (x2_streched - x1) * a) if a != 0 else x2
        if y2_streched < 0:
            y2_streched = 0

        cv2.line(output_image, (x1_streched, y1_streched), (x2_streched, y2_streched), (255, 0, 0), 2)
        edges['bottom_edge'] = (x1_streched, y1_streched, x2_streched, y2_streched)

    # cv2.imshow("Detected Vertical (Red) and Horizontal (Blue) Lines", output_image)
    # cv2.imshow("Edges", canny_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return edges

# image = cv2.imread('detected.png', cv2.IMREAD_GRAYSCALE)

# print(detect_edges(image))
