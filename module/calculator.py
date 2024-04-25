import numpy as np

def calculate_color_variety_complexity(pixel_counts):
    N = sum(pixel_counts)
    Cs = -sum(n * np.log(n/N) if n != 0 else 0 for n in pixel_counts)
    return Cs

def calculate_color_spatial_distribution_complexity(area_pixel_counts):
    N = sum(area_pixel_counts)
    Ck = -sum(n * np.log(n/N) if n != 0 else 0 for n in area_pixel_counts)
    return Ck

def calculate_area_complexity(color_complexities, color_counts):
    N = sum(color_counts)
    Cd = -sum(Ck * nk / N for Ck, nk in zip(color_complexities, color_counts))
    return Cd