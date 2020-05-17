# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
# 导入程序运行必须模块
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
# 导入designer工具生成的login模块
from demowidget import Ui_Form
from imagewidget import Img_Widget



class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self):
        super(MyMainForm, self).__init__()
        self.origin_img_widget = Img_Widget()
        self.result_img_widget = Img_Widget()
        # QMainWindow只有 centerwidget 布局，所以要依赖这个中心widget完成布局
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        self.setupUi(self)
        self.initUI()

    def getFile(self):
        return QFileDialog.getOpenFileName()

    # def open_event(self):
    #     image_name,_ = QFileDialog.getOpenFileName(self, "选择文件", "","*.jpg;;*.png;;*.jpeg")

    def initUI(self):
        # ---菜单栏---
        open_file_act = QAction(QIcon('exit.png'), '&打开', self)
        open_file_act.setShortcut('Ctrl+O')
        open_file_act.setStatusTip('Open File')
        open_file_act.triggered.connect(self.origin_img_widget.open_image)

        exit_act = QAction(QIcon('exit.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        self.statusBar()

        menubar=self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(open_file_act)
        fileMenu.addAction(exit_act)
        # ---菜单栏---

        layout=QVBoxLayout()
        layout.addWidget(self.origin_img_widget)
        layout.addWidget(self.result_img_widget)
        self.centralWidget().setLayout(layout)

        #self.addDockWidget(Qt_DockWidgetArea=Qt.LeftDockWidgetArea,origin_img_widget)

        #self.setCentralWidget(self.origin_img_widget)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上

    myWin.show()


    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
