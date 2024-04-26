import numpy as np
from tqdm import tqdm

def calculate_color_variety_complexity(color_counts, N):
    result = np.array([-1 * n * np.log10(n/N) if n != 0 else 0 for n in color_counts])
    Cs = np.sum(result)/N
    return Cs

def calculate_local_complexity(mask, labels, N):
    Ck = 0
    for label in labels:
        new_mask = (mask == label)
        n = np.sum(new_mask)
        if n > 1:
            Ck -= n*np.log10(n/N)
    return Ck
            
def calculate_area_complexity(mask, color_decoder, colors, counts, N):
    Cd = 0

    print("Calculate Area Complexity ...")
    for color, labels in tqdm(color_decoder.items()):
        color_index = colors.index(color)
        nk = counts[color_index]
        Ck = calculate_local_complexity(mask, labels, N)
        Cd += Ck*nk/N

    return Cd