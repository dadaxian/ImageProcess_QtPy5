# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
# 导入程序运行必须模块
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QPoint, QSize, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
# 导入designer工具生成的login模块
from demowidget import Ui_Form
from imagewidget import Img_Widget
import cv2


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self):
        super(MyMainForm, self).__init__()
        self.origin_img_widget = Img_Widget()
        self.setupUi(self)
        self.initUI1()

    def getFile(self):
        return QFileDialog.getOpenFileName()

    # def open_event(self):
    #     image_name,_ = QFileDialog.getOpenFileName(self, "选择文件", "","*.jpg;;*.png;;*.jpeg")

    def initUI1(self):
        open_file_act = QAction(QIcon('exit.png'), '&打开', self)
        open_file_act.setShortcut('Ctrl+O')
        open_file_act.setStatusTip('Open File')
        open_file_act.triggered.connect(self.origin_img_widget.open_image)

        exit_act = QAction(QIcon('exit.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(open_file_act)
        fileMenu.addAction(exit_act)

        self.setCentralWidget(self.origin_img_widget)

    def showImage(self, imageSrc):
        img = cv2.imread(imageSrc)  # 读取图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 1  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图

    def showImage1(self, imageSrc):
        self.graphicsView.scene_img = QGraphicsScene()
        self.imgShow = QPixmap()
        self.imgShow.load(imageSrc)
        self.imgShowItem = QGraphicsPixmapItem()
        self.imgShowItem.setPixmap(QPixmap(self.imgShow))
        # self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(8000,  8000))    //自己设定尺寸
        self.graphicsView.scene_img.addItem(self.imgShowItem)
        self.graphicsView.setScene(self.graphicsView.scene_img)
        self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(self.imgShow)))  # 图像自适应大小

        self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(self.imgShow)))  # 图像自适应大小

    @pyqtSlot()
    def on_zoomin_clicked(self):
        """
               点击缩小图像
               """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale - 0.05
        if self.zoomscale <= 0:
            self.zoomscale = 0.2
        self.item.setScale(self.zoomscale)  # 缩小图像

    @pyqtSlot()
    def on_zoomout_clicked(self):
        """
        点击方法图像
        """
        # TODO: not implemented yet
        self.zoomscale = self.zoomscale + 0.05
        if self.zoomscale >= 1.2:
            self.zoomscale = 1.2
        self.item.setScale(self.zoomscale)  # 放大图像

    # 实现pushButton_click()函数，textEdit是我们放上去的文本框的id
    def pushButton_click(self):
        self.textEdit.setText("你点击了按钮")


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    imageSrc = "C:\\Users\\GZZ\\Pictures\\Camera Roll\\DSC02063.jpg"
    myWin.showImage(imageSrc)
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_Form()
#
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
