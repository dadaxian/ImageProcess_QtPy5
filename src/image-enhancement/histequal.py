import numpy as np
import cv2 as cv


# 彩色图像全局直方图均衡化
def hisEqulColor1(img):
    # 将RGB图像转换到YCrCb空间中
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    # 将YCrCb图像通道分离
    channels = cv.split(ycrcb)
    # 对第1个通道即亮度通道进行全局直方图均衡化并保存
    cv.equalizeHist(channels[0], channels[0])
    # 将处理后的通道和没有处理的两个通道合并，命名为ycrcb
    cv.merge(channels, ycrcb)
    # 将YCrCb图像转换回RGB图像
    cv.cvtColor(ycrcb, cv.COLOR_YCR_CB2BGR, ycrcb)
    return ycrcb


# 彩色图像进行自适应直方图均衡化，代码同上的地方不再添加注释
def hisEqulColor2(img):
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    channels = cv.split(ycrcb)

    # 以下代码详细注释见官网：
    # https://docs.opencv.org/4.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])

    cv.merge(channels, ycrcb)
    cv.cvtColor(ycrcb, cv.COLOR_YCR_CB2BGR, ycrcb)
    return ycrcb


if __name__ == "__main__":
    img = cv.imread('C:\\Users\GZZ\\Pictures\\Camera Roll\\DSC02063.jpg')
    img1 = img.copy()
    img2 = img.copy()

    res1 = hisEqulColor1(img1)
    res2 = hisEqulColor2(img2)

    res = np.hstack((img, res1, res2))
    cv.imwrite('res1.jpg', res)
