import cv2

from road_recognition import road_recog
from src.tools.precess_bar import ShowProcess
from matplotlib import pyplot as plt
if __name__ == "__main__":
    video = cv2.VideoCapture("D:\\tmp\\GH011879.mp4")
    # 视频帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    # 视频总帧数
    frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
    # 视频宽度  视频高度
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 进度条
    bar=ShowProcess(frameCount,"process success!")
    # print(fps,frameCount)
    # video.set(cv2.CAP_PROP_POS_FRAMES, 200)
    # success, frame = video.read()
    # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # img1, img2, img3 = road_recog(frame)
    # # 显示图像
    # plt.figure("Image")  # 图像窗口名称
    # plt.subplot(1, 3, 1)
    # plt.imshow(img1)
    # plt.title('roi_image')  # 图像题目
    # plt.subplot(1, 3, 2)
    # plt.imshow(img2)
    # plt.axis('on')  # 关掉坐标轴为 off
    # plt.title('HoughLinesP')  # 图像题目
    # plt.subplot(1, 3, 3)
    # plt.imshow(img3)
    # plt.axis('on')  # 关掉坐标轴为 off
    # plt.title('Minimum two-in-line fit')  # 图像题目
    # plt.show()
    # 读取是否成功 视频当前帧
    success, frame = video.read()
    # 第一个参数：视频输出地址 第二个参数：视频编码格式 第三个参数：视频帧率 第四个参数：视频大小信息
    videoWriter = cv2.VideoWriter('D:\\tmp\\result.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    index=0
    while success:
        img1, img2, img3 = road_recog(frame)
        bar.show_process()
        # cv2.imshow("new video", img1)
        # cv2.waitKey(int(1000 / int(fps)))
        videoWriter.write(img3)
        success, frame = video.read()
    videoWriter.release()
    video.release()
