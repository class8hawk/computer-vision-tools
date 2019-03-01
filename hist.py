import cv2 as cv
from matplotlib import pyplot as plt
import os

def plot_demo(image):
    plt.hist(image.ravel(), 256, [0, 256])         #numpy的ravel函数功能是将多维数组降为一维数组
    plt.show()

def image_hist(image):     #画三通道图像的直方图
    color = ('b', 'g', 'r')   #这里画笔颜色的值可以为大写或小写或只写首字母或大小写混合
    for i , color in enumerate(color):
        hist = cv.calcHist([image], [i], None, [256], [0, 256])  #计算直方图
        plt.plot(hist, color)
        plt.xlim([0, 256])
    plt.show()

srcdir='live_96x96'


lists=os.listdir(srcdir)

for jpgname in lists:
    src = cv.imread(os.path.join(srcdir,jpgname))
    if src is None:
        continue

    cv.namedWindow('input_image', cv.WINDOW_NORMAL)
    cv.imshow('input_image', src)

    plot_demo(src)
    image_hist(src)

    #cv.waitKey(0)
    #cv.destroyAllWindows()