import sys

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.Qt import QPixmap, QPoint, Qt, QPainter, QIcon
from PyQt5.QtCore import QSize


class ImageBox(QWidget):
    def __init__(self):
        super(ImageBox, self).__init__()
        self.img = None
        self.img_array = None
        self.width = None
        self.height = None
        self.scaled_img = None
        self.point = QPoint(0, 0)
        self.start_pos = None
        self.end_pos = None
        self.left_click = False
        self.scale = 1

    def init_ui(self):
        self.setWindowTitle("ImageBox")

    def set_pixmap(self, ndarray):
        qimage = QtGui.QImage(ndarray.data, self.width, self.height, QtGui.QImage.Format_RGB32)
        self.scaled_img = QtGui.QPixmap.fromImage(qimage)


    def set_image(self, img_path):
        """
        open image file
        :param img_path: image file path
        :return:
        """
        self.img = QPixmap(img_path)
        self.img_array = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        self.width = self.img_array.shape[1]  # 获取图像大小
        self.height = self.img_array.shape[0]
        self.scaled_img = self.img.scaled(self.width, self.height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)



    def paintEvent(self, e):
        """
        receive paint events
        :param e: QPaintEvent
        :return:
        """
        if self.scaled_img:
            painter = QPainter()
            painter.begin(self)
            painter.scale(self.scale, self.scale)
            painter.drawPixmap(self.point, self.scaled_img)
            painter.end()

    def mouseMoveEvent(self, e):
        """
        mouse move events for the widget
        :param e: QMouseEvent
        :return:
        """
        if self.left_click:
            self.end_pos = e.pos() - self.start_pos
            self.point = self.point + self.end_pos
            self.start_pos = e.pos()
            self.repaint()

    def wheelEvent(self, event):
        mods = event.modifiers()
        # Ctrl键
        if Qt.ControlModifier == int(mods):
            angle_delta_y = event.angleDelta().y()
            # 滚轮滚动 y 的值为120/-120 x为0
            # print("y: " + str(event.angleDelta().y()))
            # print("x: " + str(event.angleDelta().x()))
            if angle_delta_y > 0:
                if self.scale < 2:
                    self.scale += 0.1
                    self.adjustSize()
                    self.update()
            else:
                if self.scale > 0.1:
                    self.scale -= 0.2
                    self.adjustSize()
                    self.update()

    def mousePressEvent(self, e):
        """
        mouse press events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        """
        mouse release events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = False


class Img_Widget(QWidget):
    def __init__(self):
        super(Img_Widget, self).__init__()

        self.setWindowTitle("Image Viewer")
        self.setFixedSize(1000, 600)

        self.open_file = QPushButton("Open Image")
        self.open_file.setToolTip("Open the image to view.")
        self.open_file.clicked.connect(self.open_image)
        self.open_file.setFixedSize(150, 30)

        self.zoom_in = QPushButton("")
        self.zoom_in.clicked.connect(self.large_click)
        self.zoom_in.setFixedSize(30, 30)
        in_icon = QIcon("./icons/zoom_in.jpg")
        self.zoom_in.setIcon(in_icon)
        self.zoom_in.setIconSize(QSize(30, 30))

        self.zoom_out = QPushButton("")
        self.zoom_out.clicked.connect(self.small_click)
        self.zoom_out.setFixedSize(30, 30)
        out_icon = QIcon("./icons/zoom_out.jpg")
        self.zoom_out.setIcon(out_icon)
        self.zoom_out.setIconSize(QSize(30, 30))

        w = QWidget(self)
        layout = QHBoxLayout()
        layout.addWidget(self.open_file)
        layout.addWidget(self.zoom_in)
        layout.addWidget(self.zoom_out)
        layout.setAlignment(Qt.AlignLeft)

        w.setLayout(layout)
        w.setFixedSize(550, 50)

        self.box = ImageBox()
        self.box.resize(500, 300)

        layout = QVBoxLayout()
        layout.addWidget(w)
        layout.addWidget(self.box)
        self.setLayout(layout)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(palette)

    def open_image(self):
        """
        select image file and open it
        :return:
        """
        img_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "*.jpg;;*.png;;*.jpeg")
        self.box.set_image(img_name)

    def large_click(self):
        """
        used to enlarge image
        :return:
        """
        if self.box.scale < 2:
            self.box.scale += 0.1
            self.box.adjustSize()
            self.update()

    def small_click(self):
        """
        used to reduce image
        :return:
        """
        if self.box.scale > 0.1:
            self.box.scale -= 0.2
            self.box.adjustSize()
            self.update()
