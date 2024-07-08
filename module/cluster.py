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

def set_color_decoder(color_decoder, mask, image):
    labels = np.unique(mask)
    for label in labels:
        target_label = np.where(mask==label)
        color = image[target_label[0][0]][target_label[1][0]]
        target_key = tuple(color.tolist())

        if target_key in color_decoder:
            color_decoder[target_key].append(label)
        else:
            color_decoder[target_key] = [label]

def add_conflict_label(conflict_label, label1, label2):
    is_add = False

    for conflict in conflict_label:
        if label1 in conflict and label2 in conflict:
            is_add = True
        elif label1 in conflict:
            conflict.append(label2)
            is_add = True
        elif label2 in conflict:
            conflict.append(label1)
            is_add = True

    if(not is_add):
        conflict_label.append([label1, label2])

def replace_conflict(mask, conflict_label):
    for conflict in conflict_label:
        target_label = min(conflict)
        for other_label in conflict:
            mask = np.where(mask == other_label, target_label, mask)
    return mask

# main function
def cluster_by_color(image):
    total_col, total_row, _ = image.shape

    # Set mask and global label
    mask = np.full((total_col, total_row), -1)
    new_label = 0
    color_decoder = {}

    conflict_label = []
    # Check label by each pixel
    for col in range(total_col):
        for row in range(total_row):

            detect_area = check_neighbor(col, row, total_col, total_row)
            same_pixels = same_color(image, detect_area, col, row)

            if is_labeled(mask, col, row):
                if len(same_pixels) != 0:
                    label = mask[col][row]

                    for [target_col, target_row] in same_pixels:
                        if mask[target_col][target_row] != -1 and mask[target_col][target_row] != label:
                            add_conflict_label(conflict_label, label, mask[target_col][target_row])
                            label_pixels(mask, same_pixels, label)
                
            else:
                same_pixels.append([col, row])
                if len(same_pixels) != 0:
                    label = -1
                    for [target_col, target_row] in same_pixels:
                        if mask[target_col][target_row] != -1:
                            if label == -1:
                                label = mask[target_col][target_row]
                            elif mask[target_col][target_row] < label:
                                label = mask[target_col][target_row]

                    if label == -1:
                        label_pixels(mask, same_pixels, new_label)
                        new_label += 1
                    else:
                        label_pixels(mask, same_pixels, label)

                else:
                    label_pixels(mask, same_pixels, new_label)
                    new_label += 1

    mask = replace_conflict(mask, conflict_label)

    set_color_decoder(color_decoder, mask, image)
    
    return mask, color_decoder