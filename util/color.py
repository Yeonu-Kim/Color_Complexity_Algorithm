import numpy as np

def get_unique_colors(img: np.ndarray):
    colors, counts = np.unique(img.reshape(-1, 3), axis=0, return_counts=True)
    unique_colors_rgb = [tuple(color) for color in colors]

    return unique_colors_rgb, counts