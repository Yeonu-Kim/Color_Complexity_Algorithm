import os
import cv2
import numpy as np
import pandas as pd

from config import Config
from util.visualizer import showImg, showHist

def calculate_color_variety_complexity(pixel_counts):
    N = sum(pixel_counts)
    Cs = -sum(n * np.log(n/N) if n != 0 else 0 for n in pixel_counts)
    return Cs

def calculate_color_spatial_distribution_complexity(area_pixel_counts):
    N = sum(area_pixel_counts)
    Ck = -sum(n * np.log(n/N) if n != 0 else 0 for n in area_pixel_counts)
    return Ck

def calculate_total_area_complexity(color_complexities, color_counts):
    N = sum(color_counts)
    Cd = -sum(Ck * nk / N for Ck, nk in zip(color_complexities, color_counts))
    return Cd

# Use all images in data folder
# You can set the data path in the config file
image_files = [os.path.join(Config.DATA_DIR, f) for f in os.listdir(Config.DATA_DIR) if os.path.isfile(os.path.join(Config.DATA_DIR, f))]

# Process each image
for image_file in image_files:
    # Load image
    image = cv2.imread(image_file)
    showImg(image)

    # # Separate areas by colors
    # colors, counts = np.unique(image.reshape(-1, 3), axis=0, return_counts=True)

    # # Calculate color variety complexity (Cs)
    # Cs = calculate_color_variety_complexity(counts)

    # # Calculate color spatial distribution complexity (Ck) for each color
    # Ck_values = []
    # for color in colors:
    #     mask = np.all(image == color, axis=-1)
    #     area_pixel_counts = np.bincount(mask.ravel())
    #     Ck = calculate_color_spatial_distribution_complexity(area_pixel_counts[1:])
    #     Ck_values.append(Ck)

    # # Calculate total area complexity (Cd)
    # Cd = calculate_total_area_complexity(Ck_values, counts)

    # # Save results to CSV
    # filename = os.path.splitext(os.path.basename(image_file))[0] + '_color_complexity.csv'
    # data = {'Color': colors.tolist(), 'Color Count': counts.tolist(), 'Ck': Ck_values}
    # df = pd.DataFrame(data)
    # df.to_csv(filename, index=False)
