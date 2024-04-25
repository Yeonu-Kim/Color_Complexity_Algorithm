import os
import cv2
import numpy as np
import pandas as pd

from config import Config
from util.visualizer import showImg, showHist
from util.color import get_unique_colors
from module.cluster import cluster_by_color
from module.calculator import calculate_color_variety_complexity, calculate_area_complexity

# Use all images in data folder
# You can set the data path in the config file
data_root = Config.DATA_DIR
image_files = [os.path.join(data_root, f) for f in os.listdir(data_root) if os.path.isfile(os.path.join(data_root, f))]

# Process each image
for image_file in image_files:
    # Load image
    image = cv2.imread(image_file)
    image = cv2.resize(image, (320, 240), interpolation=cv2.INTER_LINEAR) 
    showImg(image)

    colors, counts = get_unique_colors(image)
    showHist(counts)

    mask, color_decoder = cluster_by_color(image)

    total_pixel = image.shape[0] * image.shape[1]
    Cs = calculate_color_variety_complexity(counts, total_pixel)
    print(Cs)
    Cd = calculate_area_complexity(mask, color_decoder, colors, counts, total_pixel)
    print(Cd)

    Complexity = Cs + Cd
    print(Complexity)

# Save results to CSV
# filename = os.path.splitext(os.path.basename(image_file))[0] + '_color_complexity.csv'
# data = {'Color': colors.tolist(), 'Color Count': counts.tolist(), 'Ck': Ck_values}
# df = pd.DataFrame(data)
# df.to_csv(filename, index=False)
