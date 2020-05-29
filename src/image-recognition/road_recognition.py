import numpy as np

import random
from PIL import Image
import cv2

from matplotlib import pyplot as plt

# 使用掩膜 vertices 是掩膜区域
from removenoise import *


def region_of_interest(img, vertices):
    # 定义一个和输入图像同样大小的全黑图像mask，这个mask也称掩膜
    # 掩膜的介绍，可参考：https://www.cnblogs.com/skyfsm/p/6894685.html
    mask = np.zeros_like(img)

    # 根据输入图像的通道数，忽略的像素点是多通道的白色，还是单通道的白色
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # [vertices]中的点组成了多边形，将在多边形内的mask像素点保留，
    cv2.fillPoly(mask, [vertices], ignore_mask_color)

    # 与mask做"与"操作，即仅留下多边形部分的图像
    masked_image = cv2.bitwise_and(img, mask)

    return masked_image

# 实现把线段绘制在图像上的功能，以实现线段的可视化
def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    left_lines_x = []
    left_lines_y = []
    right_lines_x = []
    right_lines_y = []
    line_y_max = 0
    line_y_min = 999
    for line in lines:
        for x1, y1, x2, y2 in line:
            if y1 > line_y_max:
                line_y_max = y1
            if y2 > line_y_max:
                line_y_max = y2
            if y1 < line_y_min:
                line_y_min = y1
            if y2 < line_y_min:
                line_y_min = y2
            k = (y2 - y1) / (x2 - x1)
            if k < -0.3:
                left_lines_x.append(x1)
                left_lines_y.append(y1)
                left_lines_x.append(x2)
                left_lines_y.append(y2)
            elif k > 0.3:
                right_lines_x.append(x1)
                right_lines_y.append(y1)
                right_lines_x.append(x2)
                right_lines_y.append(y2)
    if left_lines_x.__len__() > 0:
        # 最小二乘直线拟合
        left_line_k, left_line_b = np.polyfit(left_lines_x, left_lines_y, 1)
        cv2.line(img,
                 (int((line_y_max - left_line_b) / left_line_k), line_y_max),
                 (int((line_y_min - left_line_b) / left_line_k), line_y_min),
                 color, thickness)
    if right_lines_x.__len__() > 0:
        right_line_k, right_line_b = np.polyfit(right_lines_x, right_lines_y, 1)
        # 根据直线方程和最大、最小的y值反算对应的x
        cv2.line(img,
                 (int((line_y_max - right_line_b) / right_line_k), line_y_max),
                 (int((line_y_min - right_line_b) / right_line_k), line_y_min),
                 color, thickness)

def draw_lines_simple(img, lines, color=[255, 0, 0], thickness=2):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness) # 将线段绘制在img上


def absSobelThreshold(gray, orient='x', thresh_min=30, thresh_max=100):
    # Convert to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Apply x or y gradient with the OpenCV Sobel() function
    # and take the absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))
    # Create a copy and apply the threshold
    binary_output = np.zeros_like(scaled_sobel)
    # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # Return the result
    return binary_output

def road_recog(img):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # binary=cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # canny 算子边缘检测
    low_threshold = 40
    high_threshold = 150
    gaussian_img = blur_gaussian_img(gray, 3)
    median_img = blur_median_img(gray, )
    canny_image = cv2.Canny(gaussian_img, low_threshold, high_threshold)
    sobel_image = absSobelThreshold(median_img, 'x', 30, 100)

    # 掩膜处理
    # 图像像素行数
    rows = canny_image.shape[0]
    # 图像像素列数
    cols = canny_image.shape[1]
    left_bottom = [-cols / 3, rows]
    right_bottom = [cols * 4 / 3, rows]
    # left_bottom = [0, rows]
    # right_bottom = [cols, rows]
    apex = [cols / 2, rows * 1 / 3]
    vertices = np.array([left_bottom, right_bottom, apex], np.int32)
    roi_image = region_of_interest(sobel_image, vertices)

    # 霍夫变换
    rho = 2  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 100  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    # Hough Transform 检测线段，线段两个端点的坐标存在lines中
    lines = cv2.HoughLinesP(roi_image, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    # 绘图
    line_image = np.copy(img)  # 复制一份原图，将线段绘制在这幅图上
    line_image_simple = np.copy(img)
    if lines is not None:
        draw_lines(line_image, lines, [255, 0, 0], 2)
        draw_lines_simple(line_image, lines, [0, 255, 0], 1)

    # result=np.concatenate((roi_image,line_image_simple),axis=1)    #x轴方向拼接
    # result=np.concatenate((result,line_image),axis=1)    #x轴方向拼接
    return roi_image,line_image_simple,line_image

if __name__ == "__main__":
    # Read image
    img = cv2.imread("C:\\Users\\GZZ\\Pictures\\Saved Pictures\\road\\3.jpg")
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    # # binary=cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #
    # # canny 算子边缘检测
    # low_threshold = 40
    # high_threshold = 150
    # gaussian_img = blur_gaussian_img(gray, 3)
    # median_img = blur_median_img(gray, )
    # canny_image = cv2.Canny(gaussian_img, low_threshold, high_threshold)
    # sobel_image=absSobelThreshold(median_img,'x',30,100)
    #
    #
    # # 掩膜处理
    # # 图像像素行数
    # rows = canny_image .shape[0]
    # # 图像像素列数
    # cols = canny_image .shape[1]
    # left_bottom = [-cols / 3, rows]
    # right_bottom = [cols*4/3, rows]
    # # left_bottom = [0, rows]
    # # right_bottom = [cols, rows]
    # apex = [cols / 2, rows*1/3]
    # vertices = np.array([left_bottom, right_bottom, apex], np.int32)
    # roi_image = region_of_interest(sobel_image, vertices)
    #
    # # 霍夫变换
    # rho = 2  # distance resolution in pixels of the Hough grid
    # theta = np.pi / 180  # angular resolution in radians of the Hough grid
    # threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    # min_line_length = 100  # minimum number of pixels making up a line
    # max_line_gap = 10  # maximum gap in pixels between connectable line segments
    # # Hough Transform 检测线段，线段两个端点的坐标存在lines中
    # lines = cv2.HoughLinesP(roi_image, rho, theta, threshold, np.array([]),
    #                         min_line_length, max_line_gap)
    #
    # # 绘图
    # line_image = np.copy(img)  # 复制一份原图，将线段绘制在这幅图上
    # line_image_simple=np.copy(img)
    #
    # draw_lines(line_image, lines, [255, 0, 0], 1)
    # draw_lines_simple(line_image_simple, lines, [255, 0, 0], 1)

    # img = cv2.imread("C:\\Users\\GZZ\\Pictures\\Camera Roll\\yhzd.jpg" ,cv2.COLOR_RGB2BGR)
    # img=Image.open("C:\\Users\\GZZ\\Pictures\\Saved Pictures\\road\\1.jpg")
    # 添加椒盐噪声，噪声比例为 0.02
    # out1 = sp_noise(img, prob=0.02)
    # 添加高斯噪声，均值为0，方差为0.001
    # out2 = gasuss_noise(img, mean=0, var=0.001)
    img1,img2,img3=road_recog(img)
    # 显示图像
    plt.figure("Image")  # 图像窗口名称
    plt.subplot(1, 3, 1)
    plt.imshow(img1)
    plt.title('roi_image')  # 图像题目
    plt.subplot(1,3,2)
    plt.imshow(img2)
    plt.axis('on')  # 关掉坐标轴为 off
    plt.title('HoughLinesP')  # 图像题目
    plt.subplot(1,3,3)
    plt.imshow(img3)
    plt.axis('on')  # 关掉坐标轴为 off
    plt.title('Minimum two-in-line fit')  # 图像题目
    plt.show()