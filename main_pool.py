import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

from config import Config
from util.visualizer import showImg, showHist
from util.color import get_unique_colors
from module.cluster import cluster_by_color
from module.calculator import calculate_color_variety_complexity, calculate_area_complexity

# Function to process each image
def process_image(image_file):
    try:
        filename, extension = os.path.basename(image_file).rsplit('.', 1)
        
        if extension.lower() not in ['jpeg', 'jpg', 'png']:
            return None
        
        # Load image
        image = cv2.imread(image_file)
        image = cv2.resize(image, Config.RESIZE, interpolation=cv2.INTER_NEAREST) 
        # showImg(image)

        colors, counts = get_unique_colors(image)
        # showHist(counts) # Set y max limitation to 1000

        mask, color_decoder = cluster_by_color(image)

        total_pixel = image.shape[0] * image.shape[1]
        Cs = calculate_color_variety_complexity(counts, total_pixel)
        Cd = calculate_area_complexity(mask, color_decoder, colors, counts, total_pixel)

        Complexity = Cs + Cd

        return [filename, Cs, Cd, Complexity, len(colors)]
    
    except Exception as e:
        print(f"Error processing {image_file}: {str(e)}")
        return None

if __name__ == '__main__':
    # Use all images in data folder
    data_root = Config.DATA_DIR
    print("Loading all images...")
    image_files = [os.path.join(data_root, f) for f in tqdm(os.listdir(data_root)) if os.path.isfile(os.path.join(data_root, f))]

    # Initialize DataFrame
    df = pd.DataFrame(columns=['name', 'Cs', 'Cd', 'Complexity', 'colors'])

    # Set up multiprocessing pool
    # num_processes = cpu_count()  # Use all available CPU cores
    num_processes = 10
    print(f"Using {num_processes} processes...")
    with Pool(num_processes) as pool:
        results = list(tqdm(pool.imap_unordered(process_image, image_files), total=len(image_files)))

    # Remove None results and add to DataFrame
    for result in results:
        if result is not None:
            df.loc[len(df)] = result

    # Save results to CSV
    output_file_path = os.path.join(Config.OUTPUT_DIR, 'output.csv')
    df.to_csv(output_file_path, index=False)
    print("Processing complete. Results saved to", output_file_path)
    print(df)
