import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from config import Config
from util.visualizer import showImg, showHist
from util.color import get_unique_colors
from module.cluster import cluster_by_color
from module.calculator import calculate_color_variety_complexity, calculate_area_complexity

# Use all images in data folder
# You can set the data path in the config file
data_root = Config.DATA_DIR
print(("Load all images..."))
image_files = [os.path.join(data_root, f) for f in tqdm(os.listdir(data_root)) if os.path.isfile(os.path.join(data_root, f))]

df = pd.DataFrame(columns=['name', 'Cs', 'Cd', 'Complexity', 'colors'])
print("Start image processing...")

# Process each image
for image_file in tqdm(image_files):
    filename, extension = os.path.basename(image_file).split('.')

    if extension != 'jpeg':
        continue

    # Load image
    image = cv2.imread(image_file)
    image = cv2.resize(image, Config.RESIZE, interpolation=cv2.INTER_NEAREST) 
    showImg(image)

    colors, counts = get_unique_colors(image)
    # showHist(counts) # Set y max limitation to 1000

    mask, color_decoder = cluster_by_color(image)

    total_pixel = image.shape[0] * image.shape[1]
    Cs = calculate_color_variety_complexity(counts, total_pixel)
    Cd = calculate_area_complexity(mask, color_decoder, colors, counts, total_pixel)

    Complexity = Cs + Cd

    df.loc[len(df)] = [filename, Cs, Cd, Complexity, len(colors)]

df.to_csv(os.path.join(Config.OUTPUT_DIR, 'output.CSV'), index=False)
print(df)
