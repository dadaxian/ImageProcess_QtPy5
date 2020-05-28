import cv2


def blur_avg_img(img,blur_size=3):
    # 均值滤波
    return cv2.blur(img, (blur_size, blur_size))

def blur_boxfilter_img(img,blur_size=3):
    # 方框滤波
    # cv2.boxFilter(原始图像, 目标图像深度, 核大小, normalize属性)
    # 其中，目标图像深度是int类型，通常用“-1”表示与原始图像一致；核大小主要包括（3，3）和（5，5）
    result = cv2.boxFilter(img, -1, (blur_size,blur_size), normalize=1)

def blur_gaussian_img(img,blur_size=3):
    # 高斯滤波
    # dst = cv2.GaussianBlur(src, ksize, sigmaX)
    # 其中，src表示原始图像，ksize表示核大小，sigmaX表示X方向方差。注意，核大小（N, N）必须是奇数，X方向方差主要控制权重。
    return cv2.GaussianBlur(img, (blur_size, blur_size),sigmaX=0)

def blur_median_img(img,blur_size=3):
    # 中值滤波
    # OpenCV主要调用medianBlur()函数实现中值滤波。图像平滑里中值滤波的效果最好。
    # dst = cv2.medianBlur(src, ksize)
    # 其中，src表示源文件，ksize表示核大小。核必须是大于1的奇数，如3、5、7等。
    return cv2.medianBlur(img, blur_size)