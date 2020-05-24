import time

import numpy as np
import cv2

# 彩色图像计算亮度
from config_src import *


def get_color_img_bright(img):
    # 将RGB图像转换到YCrCb空间中
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # 将YCrCb图像通道分离
    channels = cv2.split(ycrcb)
    # # 对第1个通道即亮度通道进行全局直方图均衡化并保存
    # cv.equalizeHist(channels[0], channels[0])
    hist = np.bincount(channels[0].ravel(), minlength=220)  # 性能：0.003163 s
    hist1, bins = np.histogram(channels[0].ravel(), 220, [16, 225])  # 性能：0.020628 s
    hist = cv2.calcHist([img], [0], None, [220], [16, 225])  # 性能：0.025288 s

    # # 将处理后的通道和没有处理的两个通道合并，命名为ycrcb
    # cv.merge(channels, ycrcb)
    # # 将YCrCb图像转换回RGB图像
    # cv.cvtColor(ycrcb, cv.COLOR_YCR_CB2BGR, ycrcb)
    return hist

# 彩色图像设置亮度
# 使用 HLS色域空间调节
def set_color_img_bright(liangdu,baohedu,img):
    start = time.clock()
    # 复制
    hlsCopy = np.copy(img)
    # 得到 l 和 s 的值
    l = liangdu
    s = baohedu
    # 1.调整亮度（线性变换) , 2.将hlsCopy[:, :, 1]和hlsCopy[:, :, 2]中大于1的全部截取
    hlsCopy[:, :, 1] = (1.0 + l/ float(MAX_VALUE_LIANGDU) ) * hlsCopy[:, :, 1]
    hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1
    # 饱和度
    hlsCopy[:, :, 2] = (1.0 + s / float(MAX_VALUE_BAOHEDU)) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    lsImg=lsImg*255
    return lsImg.astype(np.uint8)

if __name__ == "__main__":
    img = cv2.imread('C:\\Users\GZZ\\Pictures\\Camera Roll\\DSC02063.jpg')
    get_color_img_bright(img)
    # img1 = img.copy()
    # img2 = img.copy()
    #
    # res1 = hisEqulColor1(img1)
    # res2 = hisEqulColor2(img2)
    #
    # res = np.hstack((img, res1, res2))
    # cv.imwrite('res1.jpg', res)
