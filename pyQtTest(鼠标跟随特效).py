#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random,choice
import string

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtProperty

import os
from PIL import ImageGrab
import time
import pyautogui
import cv2
import numpy as np
import qtawesome

from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer
import qtawesome as qta
import requests
import traceback

from math import floor, pi, cos, sin
from random import random, randint
from time import time,sleep
import math


Desktop = "./"
Picture = "lock.png"

Style = '''
QMenu {
    /* 半透明效果 */
    /* background-color: rgba(255, 255, 255, 230); */
    background-color: white;
    border: none;
    border-radius: 4px;
}
#alphaMenu {
    background-color: rgba(255, 255, 255, 230);
}

QMenu::item {
    border-radius: 4px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 16px;
    background-color: transparent;
}

/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    /* 半透明效果 */
    /* background-color: rgba(232, 232, 232, 232); */
    background-color: rgb(232, 232, 232);
}
#alphaMenu::item:selected {
    background-color: rgba(232, 232, 232, 100);
}

/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}

/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}

/* 分割线效果 */
QMenu::separator {
    height: 1px;
    background-color: rgb(232,236,243);
}
'''

# 开机界面
class StartGif(QThread):
    # 写在这里是有讲究的,类外也用到了这个trigger
    trigger = pyqtSignal()

    def __int__(self):
        super(StartGif, self).__init__()

    def useTime(self):
        # 模拟耗时操作，一般来说耗时的加载数据应该放到线程
        for i in range(2):
            sleep(1)
            splash.showMessage('加载进度: 100%', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
            QApplication.instance().processEvents()

        splash.showMessage('初始化完成', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)

    def run(self):
        self.useTime()
        self.trigger.emit()
class GifSplashScreen(QSplashScreen):
    def __init__(self, *args, **kwargs):
        super(GifSplashScreen, self).__init__(*args, **kwargs)
        self.movie = QMovie('splash-unscreen.gif')
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.movie.start()

    def onFrameChanged(self, _):
        self.setPixmap(self.movie.currentPixmap())

    def finish(self):
        self.movie.stop()
        self.close()
        w.show()

# 桌面宠物
class Sister():
    def __init__(self,width=1400,height=800):
        self.image_key = 1
        self.image_url = 'image/meizi/meizi_ ('
        self.image = self.image_url + str(self.image_key) + ').png'
        self.birthplace = (width, height)
        self.ract_x = width
        self.ract_y = height

    def gif(self):
        if self.image_key < 61:
            self.image_key += 1
        else:
            self.image_key = 1
        self.image = self.image_url + str(self.image_key) + ').png'
class TablePet(QWidget):
    def __init__(self):
        super(TablePet, self).__init__()

        self.sister=Sister()

        self.is_follow_mouse = False

        self.initUi()

        # 每隔一段时间执行
        timer_sister = QTimer(self)
        timer_sister.timeout.connect(self.gem)
        timer_sister.start(250)
            
        #声明
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 开放右键策略
        self.customContextMenuRequested.connect(self.rightMenuShow)

    def gem(self):
        ##僵尸实现gif效果
        self.sister.gif()
        self.pm_sister= QPixmap(self.sister.image)
        self.lb_sister.setPixmap(self.pm_sister)

    def initUi(self):
        ##窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0,0,screen.width(),screen.height())

        ##僵尸标签
        self.lb_sister = QLabel(self)
        self.pm_sister= QPixmap(self.sister.image)
        self.lb_sister.setPixmap(self.pm_sister)
        self.lb_sister.move(self.sister.ract_x, self.sister.ract_y)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True

            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.sister.ract_x=QCursor.pos().x()-77
            self.sister.ract_y=QCursor.pos().y()-63
            self.lb_sister.move(self.sister.ract_x,self.sister.ract_y)
            event.accept()

    def mouseDoubleClickEvent(self,event):
        # 如果左键双击了
        if event.button() == Qt.LeftButton:
            # 让宠物说话
            self.pet_blabel = BubbleLabel()
            self.pet_blabel.setText("主人, 爱你哟^ ^")
            self.pet_blabel.show()
            # self.pet_blabel.petShow()

    # 添加右键菜单
    def rightMenuShow(self, pos):
        menu = QMenu(self)
        menu.addAction(QAction(QIcon('image/eye.png'), '隐藏', self, triggered=self.hide))
        menu.addAction(QAction(QIcon('image/exit.png'), '退出', self, triggered=self.quit))
        menu.exec_(QCursor.pos())

    def quit(self):
        self.close()
        w.show()

    def hide(self):
        self.setVisible(False)

# 鼠标跟随动画美化
# def getDistance(p1, p2):
#     return math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2)
# def findClose(points):
#     plen = len(points)
#     for i in range(plen):
#         closest = [None, None, None, None, None]
#         p1 = points[i]
#         for j in range(plen):
#             p2 = points[j]
#             dte1 = getDistance(p1, p2)
#             if p1 != p2:
#                 placed = False
#                 for k in range(5):
#                     if not placed:
#                         if not closest[k]:
#                             closest[k] = p2
#                             placed = True
#                 for k in range(5):
#                     if not placed:
#                         if dte1 < getDistance(p1, closest[k]):
#                             closest[k] = p2
#                             placed = True
#         p1.closest = closest
# class Target:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
# class Point(QObject):
#     valueChanged = pyqtSignal(int)

#     def __init__(self, x, ox, y, oy, *args, **kwargs):
#         super(Point, self).__init__(*args, **kwargs)
#         self.__x = x
#         self._x = x
#         self.originX = ox
#         self._y = y
#         self.__y = y
#         self.originY = oy
#         # 5个闭合点
#         self.closest = [0, 0, 0, 0, 0]
#         # 圆半径
#         self.radius = 2 + random() * 2
#         # 连线颜色
#         self.lineColor = QColor(156, 217, 249)
#         # 圆颜色
#         self.circleColor = QColor(156, 217, 249)

#     def initAnimation(self):
#         # 属性动画
#         if not hasattr(self, 'xanimation'):
#             self.xanimation = QPropertyAnimation(
#                 self, b'x', self, easingCurve=QEasingCurve.InOutSine)
#             self.xanimation.valueChanged.connect(self.valueChanged.emit)
#             self.yanimation = QPropertyAnimation(
#                 self, b'y', self, easingCurve=QEasingCurve.InOutSine)
#             self.yanimation.valueChanged.connect(self.valueChanged.emit)
#             self.yanimation.finished.connect(self.updateAnimation)
#             self.updateAnimation()

#     def updateAnimation(self):
#         self.xanimation.stop()
#         self.yanimation.stop()
#         duration = (1 + random()) * 1000
#         self.xanimation.setDuration(int(duration))
#         self.yanimation.setDuration(int(duration))
#         self.xanimation.setStartValue(self.__x)
#         self.xanimation.setEndValue(self.originX - 50 + random() * 100)
#         self.yanimation.setStartValue(self.__y)
#         self.yanimation.setEndValue(self.originY - 50 + random() * 100)
#         self.xanimation.start()
#         self.yanimation.start()

#     @pyqtProperty(float)
#     def x(self):
#         return self._x

#     @x.setter
#     def x(self, x):
#         self._x = x

#     @pyqtProperty(float)
#     def y(self):
#         return self._y

#     @y.setter
#     def y(self, y):
#         self._y = y

# 随机动画美化
class Circle:
    def __init__(self, background, width, height):
        # 最小和最大半径、半径阈值和填充圆的百分比
        radMin = 5
        radMax = 20
        concentricCircle = 60  # 同心圆百分比
        radThreshold = 25  # IFF special, over this radius concentric, otherwise filled
        # 最小和最大移动速度
        speedMin = 0.3
        speedMax = 0.6
        colors = [
            QColor(52, 168, 83),
            QColor(117, 95, 147),
            QColor(199, 108, 23),
            QColor(194, 62, 55),
            QColor(0, 172, 212),
            QColor(120, 120, 120)
        ]

        self.background = background
        self.x = self.randRange(-width / 2, width / 2)
        self.y = self.randRange(-height / 2, height / 2)
        self.radius = self.hyperRange(radMin, radMax)
        self.filled = (False if randint(
            0, 100) > concentricCircle else 'full') if self.radius < radThreshold else (
            False if randint(0, 100) > concentricCircle else 'concentric')
        self.color = colors[randint(0, len(colors) - 1)]
        self.borderColor = colors[randint(0, len(colors) - 1)]
        self.opacity = 0.05
        self.speed = self.randRange(speedMin, speedMax)  # * (radMin / self.radius)
        self.speedAngle = random() * 2 * pi
        self.speedx = cos(self.speedAngle) * self.speed
        self.speedy = sin(self.speedAngle) * self.speed
        spacex = abs((self.x - (-1 if self.speedx < 0 else 1) *
                      (width / 2 + self.radius)) / self.speedx)
        spacey = abs((self.y - (-1 if self.speedy < 0 else 1) *
                      (height / 2 + self.radius)) / self.speedy)
        self.ttl = min(spacex, spacey)

    # 生成随机整数 a<=x<=b
    def randint(self, a, b):
        return floor(random() * (b - a + 1) + a)
    # 生成随机小数
    def randRange(self, a, b):
        return random() * (b - a) + a
    # 生成接近a的随机小数
    def hyperRange(self, a, b):
        return random() * random() * random() * (b - a) + a

# 歌曲名称气泡提示
class BubbleLabel(QWidget):
    BackgroundColor = QColor(195, 195, 195)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        super(BubbleLabel, self).__init__(*args, **kwargs)
        # 设置无边框置顶
        self.setWindowFlags(  Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        # 设置最小宽度和高度
        self.setMinimumWidth(150)
        self.setMinimumHeight(48)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        layout = QVBoxLayout(self)
        # 左上右下的边距（下方16是因为包括了三角形）
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.setText(text)
        # 获取屏幕高宽
        self._desktop = QApplication.instance().desktop()

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.close()

    # 原本的气泡效果
    def show(self):
        super(BubbleLabel, self).show()
        # 窗口开始位置
        startPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 100,
            self._desktop.availableGeometry().height() - self.height())
        endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 100,
            self._desktop.availableGeometry().height() - self.height() * 3 - 5)
        # print(startPos, endPos)
        self.move(startPos)
        # 初始化动画
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        # 设置动画曲线
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(4000)  # 在4秒的时间内完成
        # 往上移动动画
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        moveAnimation.setDuration(5000)  # 在5秒的时间内完成
        # 并行动画组（目的是让上面的两个动画同时进行）
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        self.animationGroup.finished.connect(self.close)  # 动画结束时关闭窗口
        self.animationGroup.start()

    def paintEvent(self, event):
        super(BubbleLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        rectPath = QPainterPath()  # 圆角矩形
        triPath = QPainterPath()  # 底部三角形

        height = self.height() - 8  # 往上偏移8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 5, 5)
        x = self.width() / 5 * 4
        triPath.moveTo(x, height)  # 移动到底部横线4/5处
        # 画三角形
        triPath.lineTo(x + 6, height + 8)
        triPath.lineTo(x + 12, height)

        rectPath.addPath(triPath)  # 添加三角形到之前的矩形上

        # 边框画笔
        painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine,
                            Qt.RoundCap, Qt.RoundJoin))
        # 背景画刷
        painter.setBrush(self.BackgroundColor)
        # 绘制形状
        painter.drawPath(rectPath)
        # 三角形底边绘制一条线保证颜色与背景一样
        painter.setPen(QPen(self.BackgroundColor, 1,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(int(x), int(height), int(x + 12), int(height))

    def windowOpacity(self):
        return super(BubbleLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(BubbleLabel, self).setWindowOpacity(opacity)

    # 由于opacity属性不在QWidget中需要重新定义一个
    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)

# 异步子线程获取音乐链接
class GetMusicThread(QThread):
    # 这里设置要emit的参数类型
    finished_signal = pyqtSignal(str,str)

    def __init__(self,parent=None):
        super().__init__(parent)

    def run(self):
        reps = requests.post("https://api.uomg.com/api/rand.music?format=json")
        file_url = reps.json()['data']['url']
        file_name = reps.json()['data']['name']
        self.finished_signal.emit(file_url,file_name)

# 拒绝省电功能
class WorkThread(QThread):
    # 写在这里是有讲究的,类外也用到了这个trigger
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThread, self).__init__()

    def Image_Compare(self, picture):
        #截屏，同时提前准备一张屏幕上会出现的小图bd.png
        img = ImageGrab.grab()
        img.save(Desktop+'screen.png','png')
        #加载原始RGB图像
        img_rgb = cv2.imread(Desktop+"screen.png")
        #创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        #加载将要搜索的图像模板
        template = cv2.imread(Desktop+picture,0)
        #使用matchTemplate对原始灰度图像和图像模板进行匹配
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        #设定阈值,0.7应该可以
        threshold = 0.8
        #res大于99.9%
        loc = np.where( res >= threshold)

        flag = 0
        #得到原图像中的坐标
        for pt in zip(*loc[::-1]):
            if(pt[0] and pt[1]):
                # print(pt[0],pt[1])
                pyautogui.click(pt[0],pt[1])
                flag = 1
                break
        if(flag):
            print(picture+"capture succeess!")
        else:
            # print(picture+"capture fail!")
            pass
        
        os.remove(Desktop+'screen.png')

    def run(self):
        while(True):
            try:
                self.Image_Compare(Picture)
            except:  
                print("锁屏了,省电成功,呜呜")
                break
            # 自动锁屏大概时间间隔是5，6分钟,延时时间设为一分钟
            sleep(60*1)
        # 发出信号，如果接受到信号，说明G了，可以将按钮状态修改一下
        self.trigger.emit()

# 主窗口
class Window(QMainWindow,QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.init_ui()
        self.init_CircleLineWindow()
        self.initPlayer()
        # self.initPoints()
        self.fadeInOut()
        self.init_tpWindows()
        self.initMenu()

    def init_ui(self):
        # 设置窗体无边框
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  #窗口置顶，无边框，在任务栏不显示图标
        self.setWindowFlags(Qt.WindowStaysOnTopHint | self.windowFlags()| Qt.FramelessWindowHint |Qt.Tool)  #窗口置顶，无边框，在任务栏不显示图标
        self._width = QApplication.desktop().availableGeometry(self).width()        # 窗口靠边

        self.resize(798,489)
        # move()方法移动了窗口到屏幕坐标x=300, y=300的位置.
        # self.move(300,300)
        # 在这里我们设置了窗口的标题.标题会被显示在标题栏上.
        self.setWindowTitle('Never Lock Windows')
        # 设置左上角logo
        self.setWindowIcon(QIcon('Logo.png'))
        # 设置背景,必须要用QMainWindow,不能用QWidget
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("background.jpg")))
        self.setPalette(palette)

        ############窗口是否显示,用来控制美化粒子窗口
        self._canDraw = True

        ###################
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        
        ###################
        self.left_widget = QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')

        self.right_widget = QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:none;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列

        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        # 必须在鼠标跟随粒子上层所有的widget加上setMouseTracking(True)才行
        self.main_widget.setMouseTracking(True)
        self.right_widget.setMouseTracking(True)
        self.left_widget.setMouseTracking(True)

        ################################
        self.left_close = QPushButton("") # 关闭按钮
        self.left_visit = QPushButton("") # 空白按钮
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_close.setObjectName("关闭")
        self.left_visit.setObjectName("最大化")
        self.left_mini .setObjectName("最小化")
        self.left_close.clicked.connect(self.ButtonClick)
        self.left_visit.clicked.connect(self.ButtonClick)
        self.left_mini.clicked.connect(self.ButtonClick)

        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_label_1 = QPushButton("功能列表")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QPushButton("功能设置")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QPushButton(qtawesome.icon('fa.music',color='white'),"兆易创新")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QPushButton(qtawesome.icon('fa.sellsy',color='white'),"准入助手")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QPushButton(qtawesome.icon('fa.film',color='white'),"音乐转换")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QPushButton(qtawesome.icon('fa.home',color='white'),"时间设置")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QPushButton(qtawesome.icon('fa.download',color='white'),"启停管理")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QPushButton(qtawesome.icon('fa.heart',color='white'),"添加项目")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QPushButton(qtawesome.icon('fa.comment',color='white'),"反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0,1,1)
        self.left_layout.addWidget(self.left_close, 0, 2,1,1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)

        self.left_layout.addWidget(self.left_label_1,1,0,1,3)
        self.left_layout.addWidget(self.left_button_1, 2, 0,1,3)
        self.left_layout.addWidget(self.left_button_2, 3, 0,1,3)
        self.left_layout.addWidget(self.left_button_3, 4, 0,1,3)
        self.left_layout.addWidget(self.left_label_2, 5, 0,1,3)
        self.left_layout.addWidget(self.left_button_4, 6, 0,1,3)
        self.left_layout.addWidget(self.left_button_5, 7, 0,1,3)
        self.left_layout.addWidget(self.left_button_6, 8, 0,1,3)
        self.left_layout.addWidget(self.left_label_3, 9, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 10, 0,1,3)
        self.left_layout.addWidget(self.left_button_8, 11, 0,1,3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        #############搜索框
        self.right_bar_layout = QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_widget = QWidget() # 右侧顶部搜索框部件

        self.search_icon = QLabel(chr(0xf002) + ' '+'搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入功能, 回车进行搜索")
        self.right_bar_widget_search_input.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')

        # self.head_image = SlippedImgWidget('bg.png', 'fg.png')


        self.right_bar_layout.addWidget(self.search_icon,0,0,1,1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input,0,1,1,8)
        # self.right_bar_layout.addWidget(self.head_image,0,10,1,1)
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 4)

        ##################################
        self.right_recommend_label = QLabel("热门推荐")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QWidget() # 推荐封面部件
        self.right_recommend_layout = QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.right_recommend_widget.setStyleSheet(
        '''QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
        ''')

        self.recommend_button_1 = QToolButton()
        self.recommend_button_1.setText("打招呼") # 设置按钮文本
        self.recommend_button_1.setIcon(QIcon('Logo.png')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QSize(100,100)) # 设置图标大小
        self.recommend_button_1.setObjectName("打招呼")
        self.recommend_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        self.recommend_button_1.clicked.connect(self.ButtonClick)

        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)


        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 1)

        ############################
        self.right_newsong_lable = QLabel("拒绝锁屏")
        self.right_newsong_lable.setObjectName('right_lable')

        self.right_newsong_widget = QWidget()  # 最新歌曲部件
        self.right_newsong_layout = QGridLayout() # 最新歌曲部件网格布局
        self.right_newsong_widget.setLayout(self.right_newsong_layout)
        self.right_newsong_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:gray;
                font-size:12px;
                height:25px;
                padding-left:5px;
                padding-right:5px;
                text-align:center;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #3E80FF;
                border-radius:10px;
            }
        ''')

        self.newsong_button_1 = QPushButton("雨打梨花深闭门")
        self.newsong_button_2 = QPushButton("赏心乐事共谁论")
        self.newsong_button_3 = QPushButton("愁聚眉峰尽日颦")
        self.newsong_button_4 = QPushButton("晓看天色暮看云")
        self.newsong_button_5 = QPushButton("忘了青春误了青春")
        self.newsong_button_6 = QPushButton("花下销魂月下销魂")
        self.newsong_button_7 = QPushButton("千点啼痕万点啼痕")
        self.newsong_button_8 = QPushButton("行也思君坐也思君")
        self.newsong_button_1.setObjectName("雨打")
        self.newsong_button_2.setObjectName("赏心")
        self.newsong_button_3.setObjectName("愁聚")
        self.newsong_button_4.setObjectName("晓看")
        self.newsong_button_5.setObjectName("忘了")
        self.newsong_button_6.setObjectName("花下")
        self.newsong_button_7.setObjectName("千点")
        self.newsong_button_8.setObjectName("行也")
        self.newsong_button_1.setEnabled(True) 
        self.newsong_button_5.setEnabled(False) 
        self.newsong_button_2.setEnabled(True) 
        self.newsong_button_6.setEnabled(False) 
        self.newsong_button_3.setEnabled(True) 
        self.newsong_button_7.setEnabled(False) 
        self.newsong_button_4.setEnabled(True) 
        self.newsong_button_8.setEnabled(False) 
        self.newsong_button_1.clicked.connect(self.ButtonClick)
        self.newsong_button_2.clicked.connect(self.ButtonClick)
        self.newsong_button_3.clicked.connect(self.ButtonClick)
        self.newsong_button_4.clicked.connect(self.ButtonClick)
        self.newsong_button_5.clicked.connect(self.ButtonClick)
        self.newsong_button_6.clicked.connect(self.ButtonClick)
        self.newsong_button_7.clicked.connect(self.ButtonClick)
        self.newsong_button_8.clicked.connect(self.ButtonClick)
 
        self.right_newsong_layout.addWidget(self.newsong_button_1,0,0,) # 0行0列
        self.right_newsong_layout.addWidget(self.newsong_button_2, 1, 0, )
        self.right_newsong_layout.addWidget(self.newsong_button_3,2,0,) # 0行0列
        self.right_newsong_layout.addWidget(self.newsong_button_4, 3, 0, )
        self.right_newsong_layout.addWidget(self.newsong_button_5,0,1,) # 0行0列
        self.right_newsong_layout.addWidget(self.newsong_button_6, 1, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_7,2,1,) # 0行0列
        self.right_newsong_layout.addWidget(self.newsong_button_8, 3, 1, )

        self.right_layout.addWidget(self.right_newsong_lable, 4, 0, 1, 2)   # 占一行2列
        self.right_layout.addWidget(self.right_newsong_widget, 5, 0, 1, 2)

        ###########################
        self.right_playlist_lable = QLabel("拒绝省电")
        self.right_playlist_lable.setObjectName('right_lable')
        
        self.right_playlist_widget = QWidget() # 播放歌单部件
        self.right_playlist_layout = QGridLayout() # 播放歌单网格布局
        self.right_playlist_widget.setLayout(self.right_playlist_layout)
        self.right_playlist_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

        self.playlist_button_1 = QToolButton()
        self.playlist_button_1.setText("宠物挂件")
        self.playlist_button_1.setIcon(QIcon('Logo.png'))
        self.playlist_button_1.setIconSize(QSize(100, 100))
        self.playlist_button_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.playlist_button_1.setObjectName("宠物")
        self.playlist_button_1.clicked.connect(self.ButtonClick)

        self.right_playlist_layout.addWidget(self.playlist_button_1,0,0)

        self.right_layout.addWidget(self.right_playlist_lable, 4, 3, 1, 1)
        self.right_layout.addWidget(self.right_playlist_widget, 5, 3, 1, 1)
    
    # 随机气泡美化
    def init_CircleLineWindow(self):
        self.randomEffect = True

        self.radMin = 5
        self.radMax = 20
        self.filledCircle = 30  # 填充圆的百分比
        # 每个圆和模糊效果的最大透明度
        self.maxOpacity = 0.6

        self.circleBorder = 10
        self.backgroundLine = QColor(52, 168, 83)
        self.backgroundColor = QColor(38, 43, 46)
        self.backgroundMlt = 0.85
        self.lineBorder = 2.5
        # 最重要的是：包含它们的整个圆和数组的数目
        self.maxCircles = 8
        # 实验变量
        self.circleExp = 1
        self.circleExpMax = 1.003
        self.circleExpMin = 0.997
        self.circleExpSp = 0.00004
        self.circlePulse = False
        self.screenWidth = 870
        self.screenHeight = 489
        self._firstDraw = True
        self._timer = QTimer(self, timeout=self.update)
        self.points = []
        self.points.clear()

        # 链接的最小距离
        self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
        # 初始化点
        for _ in range(self.maxCircles * 3):
            self.points.append(Circle('', self.screenWidth, self.screenHeight))
        self.update()
        self.newsong_button_3.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
        self.newsong_button_3.setEnabled(False) 
        self.newsong_button_7.setEnabled(True) 
    def draw(self, painter):
        if self.circlePulse:
            if circleExp < self.circleExpMin or circleExp > self.circleExpMax:
                circleExpSp *= -1
            circleExp += circleExpSp
        painter.translate(self.screenWidth / 2, self.screenHeight / 2)
        if self._firstDraw:
            t = time()
        self.renderPoints(painter, self.points)
        if self._firstDraw:
            self._firstDraw = False
            # 此处有个比例关系用于设置timer的时间，如果初始窗口很小，没有比例会导致动画很快
            t = (time() - t) * 1000 * 2
            # 比例最大不能超过1920/800
            t = int(min(2.4, self.screenHeight / self.height()) * t) - 1
            t = t if t > 15 else 15  # 不能小于15s
            # print('start timer(%d msec)' % t)
            # 开启定时器
            self._timer.start(t)
    def drawCircle(self, painter, circle):
        #  circle.radius *= circleExp
        if circle.background:
            circle.radius *= self.circleExp
        else:
            circle.radius /= self.circleExp
        radius = circle.radius

        r = radius * self.circleExp
        # 边框颜色设置透明度
        c = QColor(circle.borderColor)
        c.setAlphaF(circle.opacity)

        painter.save()
        if circle.filled == 'full':
            # 设置背景刷
            painter.setBrush(c)
            painter.setPen(Qt.NoPen)
        else:
            # 设置画笔
            painter.setPen(
                QPen(c, max(1, self.circleBorder * (self.radMin - circle.radius) / (self.radMin - self.radMax))))

        # 画实心圆或者圆圈
        painter.drawEllipse(int(circle.x - r), int(circle.y - r), int(2 * r), int(2 * r))
        painter.restore()

        if circle.filled == 'concentric':
            r = radius / 2
            # 画圆圈
            painter.save()
            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(c, max(1, self.circleBorder * (self.radMin - circle.radius) / (self.radMin - self.radMax))))
            painter.drawEllipse(int(circle.x - r), int(circle.y - r), int(2 * r), int(2 * r))
            painter.restore()

        circle.x += circle.speedx
        circle.y += circle.speedy
        if (circle.opacity < self.maxOpacity):
            circle.opacity += 0.01
        circle.ttl -= 1
    def renderPoints(self, painter, circles):
        for i, circle in enumerate(circles):
            if circle.ttl < -20:
                # 重新初始化一个
                circle = Circle('', self.screenWidth, self.screenHeight)
                circles[i] = circle
            self.drawCircle(painter, circle)
        circles_len = len(circles)
        for i in range(circles_len - 1):
            for j in range(i + 1, circles_len):
                deltax = circles[i].x - circles[j].x
                deltay = circles[i].y - circles[j].y
                dist = pow(pow(deltax, 2) + pow(deltay, 2), 0.5)
                # if the circles are overlapping, no laser connecting them
                if dist <= circles[i].radius + circles[j].radius:
                    continue
                # otherwise we connect them only if the dist is < linkDist
                if dist < self.linkDist:
                    xi = (1 if circles[i].x < circles[j].x else -
                    1) * abs(circles[i].radius * deltax / dist)
                    yi = (1 if circles[i].y < circles[j].y else -
                    1) * abs(circles[i].radius * deltay / dist)
                    xj = (-1 if circles[i].x < circles[j].x else 1) * \
                         abs(circles[j].radius * deltax / dist)
                    yj = (-1 if circles[i].y < circles[j].y else 1) * \
                         abs(circles[j].radius * deltay / dist)
                    path = QPainterPath()
                    path.moveTo(circles[i].x + xi, circles[i].y + yi)
                    path.lineTo(circles[j].x + xj, circles[j].y + yj)
                    #                     samecolor = circles[i].color == circles[j].color
                    c = QColor(circles[i].borderColor)
                    c.setAlphaF(min(circles[i].opacity, circles[j].opacity)
                                * ((self.linkDist - dist) / self.linkDist))
                    painter.setPen(QPen(c, (
                        self.lineBorder * self.backgroundMlt if circles[i].background else self.lineBorder) * (
                                                (self.linkDist - dist) / self.linkDist)))
                    painter.drawPath(path)

    # # 鼠标跟随粒子美化
    # def initPoints(self):
    #     self.mouseEffect = False
    #     self.setMouseTracking(True)     # 鼠标事件被其他窗口截获了
    #     self.setAttribute(Qt.WA_Hover,True)

    #     self.resize(798, 489)
    #     self.points_new = []
    #     self.target = Target(self.width() / 2, self.height() / 2)
    #     self.points_new.clear()

    #     # 创建点
    #     stepX = self.width() / 20
    #     stepY = self.height() / 20
    #     for x in range(0, self.width(), int(stepX)):
    #         for y in range(0, self.height(), int(stepY)):
    #             ox = x + random() * stepX
    #             oy = y + random() * stepY
    #             point = Point(ox, ox, oy, oy)
    #             point.valueChanged.connect(self.update)
    #             self.points_new.append(point)
    #     # 每个点寻找5个闭合点
    #     findClose(self.points_new)
    #     # self.newsong_button_4.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
    #     self.newsong_button_4.setEnabled(True) 
    #     self.newsong_button_8.setEnabled(False) 
    # def animate(self, painter):
        # for p in self.points_new:
        #     # 检测点的范围
        #     value = abs(getDistance(self.target, p))
        #     if value < 4000:
        #         # 其实就是修改颜色透明度
        #         p.lineColor.setAlphaF(0.3)
        #         p.circleColor.setAlphaF(0.6)
        #     elif value < 20000:
        #         p.lineColor.setAlphaF(0.1)
        #         p.circleColor.setAlphaF(0.3)
        #     elif value < 40000:
        #         p.lineColor.setAlphaF(0.02)
        #         p.circleColor.setAlphaF(0.1)
        #     else:
        #         p.lineColor.setAlphaF(0)
        #         p.circleColor.setAlphaF(0)

        #     # 画线条
        #     if p.lineColor.alpha():
        #         for pc in p.closest:
        #             if not pc:
        #                 continue
        #             path = QPainterPath()
        #             path.moveTo(p.x, p.y)
        #             path.lineTo(int(pc.x), int(pc.y))
        #             painter.save()
        #             painter.setPen(p.lineColor)
        #             painter.drawPath(path)
        #             painter.restore()

        #     # 画圆
        #     painter.save()
        #     painter.setPen(Qt.NoPen)
        #     painter.setBrush(p.circleColor)
        #     painter.drawRoundedRect(QRectF(
        #         p.x - p.radius, p.y - p.radius, 2 * p.radius, 2 * p.radius), p.radius, p.radius)
        #     painter.restore()

        #     # 开启动画
        #     p.initAnimation()
    # 鼠标跟随事件和靠边停复用
    def mouseMoveEvent(self, event):
        super(Window, self).mouseMoveEvent(event)
        # 鼠标移动时更新xy坐标
        # 为了防止对随机粒子美化的干扰，加上判断
        # if self.mouseEffect==True:
        #     self.target.x = event.x()
        #     self.target.y = event.y()
        #     self.update()
        
        '''鼠标移动事件,动态调整窗口位置'''
        if event.buttons() == Qt.LeftButton and self._canMove:
            self.move(event.globalPos() - self._pos)

    # 靠边停重写的event
    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件,这个时候需要判断窗口的左边是否符合贴到左边,顶部,右边一半'''
        super(Window, self).mouseReleaseEvent(event)
        self._canMove = False
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            # 隐藏到左边
            return self.move(1 - self.width(), y)
        if y < 0:
            # 隐藏到顶部
            return self.move(x, 1 - self.height())
        if x > self._width - self.width() / 2:  # 窗口进入右边一半距离
            # 隐藏到右边
            return self.move(self._width - 1, y)
    def enterEvent(self, event):
        '''鼠标进入窗口事件,用于弹出显示窗口'''
        super(Window, self).enterEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            return self.move(0, y)
        if y < 0:
            return self.move(x, 0)
        if x > self._width - self.width() / 2:
            return self.move(self._width - self.width(), y)
    def leaveEvent(self, event):
        '''鼠标离开事件,如果原先窗口已经隐藏,并暂时显示,此时离开后需要再次隐藏'''
        super(Window, self).leaveEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x == 0:
            return self.move(1 - self.width(), y)
        if y == 0:
            return self.move(x, 1 - self.height())
        if x == self._width - self.width():
            return self.move(self._width - 1, y)
    def mousePressEvent(self, event):
        '''鼠标按下事件,需要记录下坐标self._pos 和 是否可移动self._canMove'''
        super(Window, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.globalPos() - self.pos()
            # 当窗口最大化或者全屏时不可移动
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    # 尝试共用三个Event
    def showEvent(self, event):
        self._canDraw = True
    def hideEvent(self, event):
        # 窗口最小化要停止绘制, 减少cpu占用
        self._canDraw = False
    def paintEvent(self, event):
        super(Window, self).paintEvent(event)
        if not self._canDraw: 
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.draw(painter)
        # if (self.mouseEffect==False and self.randomEffect==False):
        #     return
        # elif (self.randomEffect==True and self.mouseEffect==False):
        #     painter = QPainter(self)
        #     painter.setRenderHint(QPainter.Antialiasing)
        #     painter.setRenderHint(QPainter.SmoothPixmapTransform)
        #     self.draw(painter)
        # elif (self.randomEffect==False and self.mouseEffect==True):
        #     painter1 = QPainter()
        #     painter1.begin(self)
        #     painter1.setRenderHint(QPainter.Antialiasing)
        #     painter1.setRenderHint(QPainter.SmoothPixmapTransform)
        #     self.animate(painter1)
        #     painter1.end()
        # else:
        #     painter = QPainter(self)
        #     painter.setRenderHint(QPainter.Antialiasing)
        #     painter.setRenderHint(QPainter.SmoothPixmapTransform)
        #     self.draw(painter)
        #     painter1 = QPainter()
        #     painter1.begin(self)
        #     painter1.setRenderHint(QPainter.Antialiasing)
        #     painter1.setRenderHint(QPainter.SmoothPixmapTransform)
        #     self.animate(painter1)
        #     painter1.end()
    
    # 初始化播放器
    def initPlayer(self):
        self.playing = False # 播放状态初始化为否
        self.player = QMediaPlayer(self)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.check_music_status)
        # 歌曲名称气泡
        self.blabel = BubbleLabel()
        # 音乐状态按钮
        self.status_label = QLabel("")
        self.status_label.setFixedSize(15,15)
        # 初始化一个歌曲列表
        self.content = QMediaContent()
        # 上一首按钮
        self.before_btn = QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        self.before_btn.setObjectName("before_btn")
        self.before_btn.clicked.connect(self.before_music)
        # 播放按钮
        self.play_btn = QPushButton(qtawesome.icon('fa.play', color='#F76677', font=18), "")
        self.play_btn.setIconSize(QSize(30, 30))
        # self.play_btn.setFixedSize(82,82)
        self.play_btn.setObjectName("play_btn")
        self.play_btn.clicked.connect(self.play_music)
        # 下一首按钮
        self.next_btn = QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
        self.next_btn.setObjectName("next_btn")
        self.next_btn.clicked.connect(self.next_music)
        # 进度条
        self.process_bar = QProgressBar()
        # self.right_process_bar.setValue(0)      # 初始进度
        self.process_value = 0                    # 初始进度
        self.process_bar.setValue(self.process_value)
        self.process_bar.setFixedHeight(3)
        self.process_bar.setTextVisible(False)   # 不显示进度条文字
        self.process_bar.setStyleSheet("QProgressBar::chunk{background:#F76677}")

        self.right_playconsole_widget = QWidget()  # 播放控制部件
        self.right_playconsole_layout = QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)
        self.right_playconsole_layout.addWidget(self.before_btn, 0, 0)
        self.right_playconsole_layout.addWidget(self.next_btn, 0, 2)
        self.right_playconsole_layout.addWidget(self.play_btn, 0, 1)
        self.right_playconsole_layout.setAlignment(Qt.AlignCenter)  # 设置布局内部件居中显示
        self.right_layout.addWidget(self.process_bar, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)
    def before_music(self):
        # 设置状态为黄色
        self.status_label.setStyleSheet('''
            QLabel{
                background:#F7D674;
                border-radius:5px;
                }
        ''')
        self.playing = True # 设置播放状态为是
        self.play_btn.setIcon(qta.icon("fa.pause",color='#F76677', font=18)) # 修改播放图标
        self.process_value = 0 # 重置进度值
        # 获取前一首歌曲必须放在调用next_music之前
        self.player.setMedia(self.temp_music)
        self.player.setVolume(50)
        self.player.play()
        self.duration = self.player.duration()  # 音乐的时长
        # 设置状态为绿色
        self.status_label.setStyleSheet('''
            QLabel{
                background:#6DDF6D;
                border-radius:5px;
                }
        ''')

        # 进度条计时器
        self.process_timer = QTimer()
        self.process_timer.setInterval(1000)
        self.process_timer.start()
        self.process_timer.timeout.connect(self.process_timer_status)
    def play_music(self):
        try:
            # 播放音乐
            if self.playing is False:
                self.playing = True # 设置播放状态为是
                self.play_btn.setIcon(qta.icon("fa.pause", color='#F76677', font=18)) # 设置播放图标
                player_status = self.player.mediaStatus() # 获取播放器状态

                if player_status == 6:
                    # 设置状态标签为绿色
                    self.status_label.setStyleSheet('''QLabel{background:#6DDF6D;border-radius:5px;}''')
                    self.player.play()
                    # 暂停之后再打开，还会提示一次
                    self.blabel.setText("继续播放:  "+ self.music_name)
                    self.blabel.show()
                else:
                    self.next_music()
            # 暂停音乐
            else:
                # 设置状态为蓝色
                self.status_label.setStyleSheet('''QLabel{background:#0099CC;border-radius:5px;}''')
                self.playing = False
                self.play_btn.setIcon(qta.icon("fa.play",color='#F76677', font=18))
                self.player.pause()
        except Exception as e:
            print(repr(e))
    def next_music(self):
        # 获取前一首歌曲
        self.temp_music = self.content
        try:
            # 设置状态为黄色
            self.status_label.setStyleSheet('''
                QLabel{
                    background:#F7D674;
                    border-radius:5px;
                    }
            ''')
            self.playing = True # 设置播放状态为是
            self.play_btn.setIcon(qta.icon("fa.pause",color='#F76677', font=18)) # 修改播放图标
            self.process_value = 0 # 重置进度值

            # 获取网络歌曲
            self.get_music_thread = GetMusicThread()
            self.get_music_thread.finished_signal.connect(self.init_player)
            self.get_music_thread.start()
        except Exception as e:
            print(traceback.print_exc())
    def init_player(self,url,music_name):
        # print("获取到音乐链接：",url)
        self.content = QMediaContent(QUrl(url))
        self.player.setMedia(self.content)
        self.player.setVolume(50)
        self.player.play()
        self.music_name = music_name

        # 第一次打开音乐
        self.blabel.setText("歌曲名称:  "+ self.music_name)
        self.blabel.show()

        self.duration = self.player.duration()  # 音乐的时长
        # 设置状态为绿色
        self.status_label.setStyleSheet('''
            QLabel{
                background:#6DDF6D;
                border-radius:5px;
                }
        ''')

        # 进度条计时器
        self.process_timer = QTimer()
        self.process_timer.setInterval(1000)
        self.process_timer.start()
        self.process_timer.timeout.connect(self.process_timer_status)
    def check_music_status(self):
        player_status = self.player.mediaStatus()
        player_duration = self.player.duration()
        # print("音乐时间：",player_duration)
        # print("当前播放器状态",player_status)
        if player_status == 7:
            self.next_music()

        if player_duration > 0:
            self.duration = player_duration
    def process_timer_status(self):
        try:
            if self.playing is True:
                self.process_value += (100 / (self.duration/1000))
                # print("当前进度：",self.process_value)
                self.process_bar.setValue(int(self.process_value))
        except Exception as e:
            # print(repr(e))
            pass

    # 界面右键menu
    def contextMenuEvent(self, event):
        self._contextMenu.exec_(event.globalPos())
    def hello(self):
        QApplication.instance().aboutQt()
    def getIcon(self):
        # 测试模拟图标,PyQt5 使用 webdings,Wingdings 字体来替代某些常用图片
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(QFont('Webdings', 11))
        painter.drawText(0, 0, 16, 16, Qt.AlignCenter,choice(string.ascii_letters))
        painter.end()
        return QIcon(pixmap)
    def initMenu(self):
        self._contextMenu = QMenu(self)
        # 背景透明
        self._contextMenu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self._contextMenu.setWindowFlags(self._contextMenu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self._contextMenu.addAction('菜单1', self.hello)
        self._contextMenu.addAction('菜单菜单2', self.hello).setEnabled(False)
        self._contextMenu.addAction(self.getIcon(), '菜单3', self.hello)
        self._contextMenu.addSeparator()

        # 二级菜单
        menu2 = QMenu('菜单菜单菜单4', self._contextMenu)  # 背景透明
        menu2.setObjectName('alphaMenu')  # 半透明演示
        menu2.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        menu2.setWindowFlags(menu2.windowFlags() |
                             Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        menu2.addAction(self.getIcon(), '子菜单1')
        menu2.addAction(self.getIcon(), '子菜单2')
        menu2.addAction(self.getIcon(), '子菜单3')
        self._contextMenu.addMenu(menu2)

        self._contextMenu.addAction(self.getIcon(), '菜单5', self.hello)
        self._contextMenu.addAction(self.getIcon(), '菜单6', self.hello)

    # Tp WINDOWS
    def init_tpWindows(self):
        # 在系统托盘处显示图标
        self.tp = QSystemTrayIcon(self)
        self.tp.setIcon(QIcon('Logo.png'))
        # 设置系统托盘图标的菜单(右击的功能),注意，这里全部要加self.不然不属于会报错
        self.a1 = QAction('显示(Show)',triggered = self.show)
        self.a2 = QAction('退出(Exit)',triggered = self.quitApp) # 直接退出可以用qApp.quit
        self.tpMenu = QMenu()
        self.tpMenu.addAction(self.a1)
        self.tpMenu.addAction(self.a2)
        self.tp.setContextMenu(self.tpMenu)
        # 不调用show不会显示系统托盘
        self.tp.show()
        # 参数1：标题 参数2：内容 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        self.tp.showMessage('启动','Never Lock Windows',icon=1)
        # 当弹窗被点击的时候
        self.tp.messageClicked.connect(self.message)
        # 图标被单击和双击时
        self.tp.activated.connect(self.act)
    def message(self):
        print("弹出的信息被点击了")
    def quitApp(self):
        self.show() # w.hide() #隐藏
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。 
            self.tp.setVisible(False)
    def act(self,reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 :
            self.doShow()
        elif reason == 3:
            self.show()

    # 窗口淡入淡出函数
    def fadeInOut(self):
        # 窗口透明度动画类
        self.fadeInOutAnimation = QPropertyAnimation(self, b'windowOpacity')
        self.fadeInOutAnimation.setDuration(1000)  # 持续时间1秒
        # 执行淡入
        self.doShow()
    def doShow(self):
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.fadeInOutAnimation.finished.disconnect(self.close)
        except:
            pass
        self.fadeInOutAnimation.stop()
        # 透明度范围从0逐渐增加到1
        self.fadeInOutAnimation.setStartValue(0)
        self.fadeInOutAnimation.setEndValue(1)
        self.fadeInOutAnimation.start()
    def doClose(self):
        self.fadeInOutAnimation.stop()
        self.fadeInOutAnimation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.fadeInOutAnimation.setStartValue(1)
        self.fadeInOutAnimation.setEndValue(0)
        self.fadeInOutAnimation.start()

    # 抖动窗口打招呼，下面这个方法可以做成这样的封装给任何控件
    def doShakeWindow(self, target):
        """窗口抖动动画
        :param target:        目标控件
        """
        if hasattr(target, '_shake_animation'):
            # 如果已经有该对象则跳过
            return

        shakeAnimation = QPropertyAnimation(target, b'pos', target)
        target._shake_animation = shakeAnimation
        shakeAnimation.finished.connect(lambda: delattr(target, '_shake_animation'))

        pos = target.pos()
        x, y = pos.x(), pos.y()

        shakeAnimation.setDuration(200)
        shakeAnimation.setLoopCount(2)
        shakeAnimation.setKeyValueAt(0, QPoint(x, y))
        shakeAnimation.setKeyValueAt(0.09, QPoint(x + 2, y - 2))
        shakeAnimation.setKeyValueAt(0.18, QPoint(x + 4, y - 4))
        shakeAnimation.setKeyValueAt(0.27, QPoint(x + 2, y - 6))
        shakeAnimation.setKeyValueAt(0.36, QPoint(x + 0, y - 8))
        shakeAnimation.setKeyValueAt(0.45, QPoint(x - 2, y - 10))
        shakeAnimation.setKeyValueAt(0.54, QPoint(x - 4, y - 8))
        shakeAnimation.setKeyValueAt(0.63, QPoint(x - 6, y - 6))
        shakeAnimation.setKeyValueAt(0.72, QPoint(x - 8, y - 4))
        shakeAnimation.setKeyValueAt(0.81, QPoint(x - 6, y - 2))
        shakeAnimation.setKeyValueAt(0.90, QPoint(x - 4, y - 0))
        shakeAnimation.setKeyValueAt(0.99, QPoint(x - 2, y + 2))
        shakeAnimation.setEndValue(QPoint(x, y))

        shakeAnimation.start(shakeAnimation.DeleteWhenStopped)

    # 如果拒绝锁屏功能因为锁屏导致的退出，捕获该信号
    def lockWindows(self):
        self.newsong_button_1.setStyleSheet('''
            QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
            QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
        ''')
        self.newsong_button_1.setEnabled(True) 
        self.newsong_button_5.setEnabled(False) 
    # 定时锁屏timeout槽函数
    def overTime(self):
        # 直接干掉线程
        self.timeLockWindows.terminate()
        self.newsong_button_2.setStyleSheet('''
            QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
            QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
        ''')            
        self.newsong_button_2.setEnabled(True) 
        self.newsong_button_6.setEnabled(False) 


    # 按钮事件
    def ButtonClick(self):  
        # 左上角三个按钮功能
        if(self.sender().objectName() == "最小化"):
            self.showMinimized()
        elif(self.sender().objectName() == "最大化"):
            if(self.isMaximized()):
                self.resize(870,489)
                self.move(300,300)
            else:
                self.showMaximized()
        elif(self.sender().objectName() == "关闭"):
            self.doClose()

        # 拒绝锁屏功能
        elif(self.sender().objectName() == "雨打"):
            self.neverLockWindows = WorkThread()
            # 增加信号接收器
            self.neverLockWindows.trigger.connect(self.lockWindows)
            self.neverLockWindows.start()
            self.newsong_button_1.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
            self.newsong_button_1.setEnabled(False) 
            self.newsong_button_5.setEnabled(True) 
        elif(self.sender().objectName() == "忘了"):
            self.neverLockWindows.terminate()
            self.newsong_button_1.setStyleSheet('''
                QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
                QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
            ''')
            self.newsong_button_1.setEnabled(True) 
            self.newsong_button_5.setEnabled(False) 

        # 准备设置成定时锁屏功能
        elif(self.sender().objectName() == "赏心"):
            self.timeLockWindows = WorkThread()
            self.timeLockWindows.start()
            self.newsong_button_2.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
            self.newsong_button_2.setEnabled(False) 
            self.newsong_button_6.setEnabled(True) 
            # 创建一个QTimer，连接timeout()信号到适当的槽函数，并调用start()，然后在恒定的时间间隔会发射timeout()信号。
            self.timeLockWindowsTimer = QTimer()
            self.timeLockWindowsTimer.timeout.connect(self.overTime)
            self.timeLockWindowsTimer.start(1000)  # 1秒

        elif(self.sender().objectName() == "花下"):
            self.timeLockWindows.terminate()
            self.newsong_button_2.setStyleSheet('''
                QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
                QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
            ''')            
            self.newsong_button_2.setEnabled(True) 
            self.newsong_button_6.setEnabled(False) 

        # 设置成背景circle-line-windows美化控制
        elif(self.sender().objectName() == "愁聚"):
            self.randomEffect = True
            self._timer.start()
            self.points.clear()
            self.update()
            # 链接的最小距离
            self.linkDist = min(self.screenWidth, self.screenHeight) / 2.4
            # 初始化点
            for _ in range(self.maxCircles * 3):
                self.points.append(Circle('', self.screenWidth, self.screenHeight))
            self.update()
            self.newsong_button_3.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
            self.newsong_button_3.setEnabled(False) 
            self.newsong_button_7.setEnabled(True) 
        elif(self.sender().objectName() == "千点"):
            self.randomEffect = False
            self._timer.stop()
            self.points.clear()
            self.update()
            self.newsong_button_3.setStyleSheet('''
                QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
                QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
            ''')            
            self.newsong_button_3.setEnabled(True) 
            self.newsong_button_7.setEnabled(False) 
   
        # 设置成背景鼠标跟随美化控制
        elif(self.sender().objectName() == "晓看"):
            self.mouseEffect = True
            self.newsong_button_4.setStyleSheet('''QPushButton{ color:black;border:1px solid #F4DED5; border-radius:10px;}''')
            self.newsong_button_4.setEnabled(False) 
            self.newsong_button_8.setEnabled(True) 
        elif(self.sender().objectName() == "行也"):
            self.mouseEffect = False
            self.newsong_button_4.setStyleSheet('''
                QPushButton{border:none;color:gray;font-size:12px;height:25px;padding-left:5px;padding-right:5px;text-align:center;}
                QPushButton:hover{color:black;border:1px solid #3E80FF;border-radius:10px;}
            ''')            
            self.newsong_button_4.setEnabled(True) 
            self.newsong_button_8.setEnabled(False) 

        # 打招呼
        elif(self.sender().objectName() == "打招呼"):
            self.doShakeWindow(self)
            self.temp_blabel = BubbleLabel()
            self.temp_blabel.setText("早上好呀^ ^")
            self.temp_blabel.show()
        
        # 宠物
        elif(self.sender().objectName() == "宠物"):
            self.close()
            self.pet=TablePet()

if __name__ == '__main__':
    import sys
    import cgitb
    cgitb.enable(1, None, 5, '')
    # pyqt窗口必须在QApplication方法中使用 
    # 每一个PyQt5应用都必须创建一个应用对象.sys.argv参数是来自命令行的参数列表.Python脚本可以从shell里运行.这是我们如何控制我们的脚本运行的一种方法.
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    # 关闭所有窗口,也不关闭应用程序
    global splash
    splash = GifSplashScreen()
    splash.show()
    splash.showMessage('等待创建界面', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
    tmp = StartGif()
    tmp.start()
    tmp.trigger.connect(splash.finish)

    QApplication.setQuitOnLastWindowClosed(False)
    w = Window()
    # w.show()
    sys.exit(app.exec_())
