import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def draw_reference_lines(image, step=20):
    height, width = image.shape[:2]

    for x in range(0, width, step):
        cv2.line(image, (x, 0), (x, height), (255, 255, 0), 1)

    for y in range(0, height, step):
        cv2.line(image, (0, y), (width, y), (255, 255, 0), 1)
    
    return image

def select_circle_roi(image_with_grid, original_image):
    r = cv2.selectROI(image_with_grid)
    cv2.destroyAllWindows()
    
    x, y, w, h = r
    cx, cy = x + w // 2, y + h // 2
    radius = min(w, h) // 2

    mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (cx, cy), radius, (255, 255, 255), -1)
    masked_image = cv2.bitwise_and(original_image, original_image, mask=mask)
        
    return masked_image

def convert_to_gray_and_blackhat(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (23, 23))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    return blackhat

def apply_threshold(image):
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def remove_noise(image):
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    return opening
 

def prepare_for_watershed(image):
    sure_bg = cv2.dilate(image, np.ones((3,3), np.uint8), iterations=3)
    
    dist_transform = cv2.distanceTransform(image, cv2.DIST_L2, 5) 

    threshold_percentage = 0.3
    _, sure_fg = cv2.threshold(dist_transform, threshold_percentage * dist_transform.max(), 255, 0)
    
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    cv2.imshow('test', sure_fg)

    return sure_fg, unknown

def apply_watershed(image, sure_fg, unknown):
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)

    boundaries_image = image.copy()
    boundaries_image[markers == -1] = [255, 0, 0]

    centers_image = image.copy()
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(sure_fg)
    
    for i in range(1, num_labels):
        cX, cY = int(centroids[i][0]), int(centroids[i][1])
        cv2.circle(centers_image, (cX, cY), 2, (255, 255, 0), -1)
        #cv2.putText(centers_image, str(i), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    n_colonies = num_labels - 1
    return boundaries_image, centers_image, n_colonies

def resize_image(image, max_side=1500):
    h, w = image.shape[:2]

    scale = max_side / max(h, w)
    if scale < 1:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image

def main():
    image_path = select_image()
    image = cv2.imread(image_path)
    image = resize_image(image,1500)
    cv2.imshow('Resized Image', image)
    cv2.waitKey(0)

    grid = draw_reference_lines(image.copy())
    cropped_image = select_circle_roi(grid,image)
    cv2.imshow('Cropped Image', cropped_image)
    cv2.waitKey(0)
    
    blackhat_image = convert_to_gray_and_blackhat(cropped_image)
    cv2.imshow('blackhat_image', blackhat_image)
    cv2.waitKey(0)
    
    binary_image = apply_threshold(blackhat_image)
    cv2.imshow('binary_image', binary_image)
    cv2.waitKey(0)

    #binary_image = remove_noise(binary_image)
    #cv2.imshow('Denoised Image', binary_image)
    #cv2.waitKey(0)

    sure_fg, unknown = prepare_for_watershed(binary_image)
    

    cropped_image = resize_image(cropped_image,5500)
    sure_fg = resize_image(sure_fg,5500)
    boundaries_image, centers_image, n_colonies = apply_watershed(cropped_image, sure_fg, unknown)
    print(f"num: {n_colonies}")

    boundaries_image = resize_image(boundaries_image,1500)
    centers_image = resize_image(centers_image,1500)

    #cv2.imshow('Boundaries', boundaries_image)
    cv2.imshow('Centers', centers_image)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
