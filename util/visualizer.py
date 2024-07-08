import matplotlib.pyplot as plt
import numpy as np

def showImg(img: np.ndarray):
    plt.imshow(img)
    plt.show()

def showHist(data: np.ndarray):
    plt.hist(data, bins=50)
    plt.ylim([0, 1000])
    plt.show()