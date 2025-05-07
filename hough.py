import cv2
import numpy as np
import os

def hough_transform(path, divisions=180, max_lines=100, freq_threshold=0, rho_thresh=20, theta_thresh=np.pi/90, max_gap=5):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(smoothed_image, threshold1=50, threshold2=125)
    h, w = edges.shape
    max_dist = int(np.hypot(h, w))
    parameter_space = [[0 for i in range(divisions)] for i in range(2*max_dist)]
    thetas = np.linspace(0, np.pi, divisions)
    for y in range(h):
        for x in range(w):
            if edges[y][x]:
                for t_idx in range(divisions):
                    theta = thetas[t_idx]
                    rho = int(round(x * np.cos(theta) + y * np.sin(theta))) + max_dist
                    parameter_space[rho][t_idx] += 1
    candidates = []
    for r in range(len(parameter_space)):
        for t in range(len(parameter_space[0])):
            freq = parameter_space[r][t]
            if freq >= freq_threshold:
                rho = r - max_dist
                theta = thetas[t]
                candidates.append((freq, rho, theta))

    candidates.sort(reverse=True)

    selected = []
    for freq, rho, theta in candidates:
        similar = False
        for _, rho2, theta2 in selected:
            if abs(rho - rho2) < rho_thresh and abs(theta - theta2) < theta_thresh:
                similar = True
                break
        if not similar:
            selected.append((freq, rho, theta))
        if len(selected) >= max_lines:
            break

    image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    edge_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    for _, rho, theta in selected:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 100000 * (-b)), int(y0 + 100000 * (a)))
        pt2 = (int(x0 - 100000 * (-b)), int(y0 - 100000 * (a)))
        inside, clipped_pt1, clipped_pt2 = cv2.clipLine((0, 0, w, h), pt1, pt2)
        if inside:
            cv2.line(image_color, clipped_pt1, clipped_pt2, (0, 0, 255), 2)

        line_points = []
        for d in range(-max(h, w), max(h, w), 1):
            x = int(round(x0 + d * (-b)))
            y = int(round(y0 + d * (a)))
            if 0 <= x < w and 0 <= y < h:
                if edges[y, x]:
                    line_points.append((x, y))

        if len(line_points) > 1:
            grouped = [[line_points[0]]]
            for i in range(1, len(line_points)):
                prev = line_points[i - 1]
                curr = line_points[i]
                if np.hypot(curr[0] - prev[0], curr[1] - prev[1]) <= max_gap:
                    grouped[-1].append(curr)
                else:
                    grouped.append([curr])

            for group in grouped:
                if len(group) >= 2:
                    for i in range(len(group) - 1):
                        cv2.line(edge_color, group[i], group[i+1], (0, 0, 255), 2)

    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    output1 = os.path.join("static/images/outputs", f"{name}_lines{ext}")
    output2 = os.path.join("static/images/outputs", f"{name}_linked{ext}")
    cv2.imwrite(output1, image_color)
    cv2.imwrite(output2, edge_color)
    return output1, output2
