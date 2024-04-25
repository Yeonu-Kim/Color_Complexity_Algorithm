import cv2
import numpy as np
from tqdm import tqdm

# Load an image
# image = cv2.imread("./data/test_street.png")

def check_neighbor(col, row, total_col, total_row):
    detect_cols = np.array([col-1, col+1])
    detect_rows = np.array([row-1, row+1])

    detect_cols = np.array([val for val in detect_cols if 0 <= val < total_col])
    detect_rows = np.array([val for val in detect_rows if 0 <= val < total_row])

    detect_area = np.array([[detect_col, row] for detect_col in detect_cols] + \
                  [[col, detect_row] for detect_row in detect_rows])
    
    return detect_area

def is_labeled(mask, col, row):
    return mask[col][row] != -1

def same_color(image, detect_area, col, row):
    color = image[col][row]
    same_colors = []
    for [target_col, target_row] in detect_area:
        target_color = image[target_col][target_row]

        if np.array_equal(target_color, color):
            same_colors.append([target_col, target_row])

    return same_colors

def label_pixels(mask, same_pixels, label):
    for [target_col, target_row] in same_pixels:
        mask[target_col][target_row] = label

# main function
def cluster_by_color(image):
    total_col, total_row, _ = image.shape

    # Set mask and global label
    mask = np.full((total_col, total_row), -1)
    new_label = 0

    print("Start masking ...")
    # Check label by each pixel
    for col in tqdm(range(total_col)):
        for row in range(total_row):
            pixel = image[col][row]

            detect_area = check_neighbor(col, row, total_col, total_row)
            same_pixels = same_color(image, detect_area, col, row)

            if is_labeled(mask, col, row):
                if len(same_pixels) != 0:
                    label = mask[col][row]
                    label_pixels(mask, same_pixels, label)
                
            else:
                same_pixels.append([col, row])
                if len(same_pixels) != 0:
                    label_pixels(mask, same_pixels, new_label)
                    new_label += 1

                else:
                    for [target_col, target_row] in same_pixels:
                        if mask[target_col][target_row] != -1:
                            label = mask[target_col][target_row]
                            label_pixels(mask, same_pixels, label)
                            break
                    
                    if mask[col][row] == -1:
                        label_pixels(mask, same_pixels, new_label)
                        new_label += 1

    print(mask)
    return mask
