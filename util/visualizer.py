import matplotlib.pyplot as plt
import numpy.typing as npt

def showImg(img: npt.NDArray):
    plt.imshow(img)
    plt.show()

def showHist(data: npt.NDArray):
    plt.hist(data)
    plt.show()