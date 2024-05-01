import numpy as np
from tqdm import tqdm

def calculate_color_variety_complexity(color_counts, N):
    result = np.array([-1 * n * np.log10(n/N) if n != 0 else 0 for n in color_counts])
    Cs = np.sum(result)/N
    return Cs

def calculate_local_complexity(mask, labels, N):
    Ck = 0
    label_counts = np.array([np.count_nonzero(mask == label) for label in labels])
    Ck -= np.sum(label_counts * np.log10(label_counts/N))
    # relevant_counts = label_counts[label_counts > 0]
    # if len(relevant_counts) > 0:
        
    return Ck
            
def calculate_area_complexity(mask, color_decoder, colors, counts, N):
    color_decoder = {color: color_decoder[color] for color in colors}
    print("Calculate spatial complexity ...")
    spatial_complexity = [calculate_local_complexity(mask, labels, counts[colors.index(color)]) \
                          for color, labels in tqdm(color_decoder.items())]
    Cd = np.sum(spatial_complexity*counts/N)

    # print("Calculate Area Complexity ...")
    # for color, labels in tqdm(color_decoder.items()):
    #     color_index = colors.index(color)
    #     nk = counts[color_index]
    #     Ck = calculate_local_complexity(mask, labels, nk)
    #     Cd += Ck*nk/N

    return Cd