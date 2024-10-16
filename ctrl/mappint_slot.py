import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QTransform, QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame, QLayout, QSizePolicy

# import main

_self = None
_self_label = None
labels = []


class DraggableLabel(QLabel):
    w = 0
    h = 0
    image_flag = 0
    image = None
    xx = 10
    yy = 10
    rotate_flag = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlignment(Qt.AlignCenter)
        self.move(self.xx, self.yy)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            print("Label position when clicked:", self.pos())
            width = self.size().width()
            height = self.size().height()

            print("Label width:", width)
            print("Label height:", height)
            if self.rotate_flag == 0:
                _self.lineEdit_5.setText(str(self.w))
                _self.lineEdit_6.setText(str(self.h))
            else:
                _self.lineEdit_5.setText(str(self.h))
                _self.lineEdit_6.setText(str(self.w))
            global _self_label
            _self_label = self

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("mouseRelease")
            print(self.pos())
            self.xx = self.x()
            self.yy = self.y()
            print(self.x(), self.y())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset is not None:
            # self.move(self.pos() + event.pos())
            # self.offset = event.pos()
            # print("Label position when dragged:", self.pos())
            x, y = event.pos().x(), event.pos().y()
            offset_x, offset_y = self.offset.x(), self.offset.y()
            new_x, new_y = x - offset_x, y - offset_y

            # 将移动差值调整为25的整数倍
            new_x = new_x - (new_x % 10)
            new_y = new_y - (new_y % 10)

            self.move(self.x() + new_x, self.y() + new_y)

    def init(self):
        # self.resize(h, w)
        # global _self_label
        # _self_label = self
        # change_label_size()
        self.move(self.xx, self.yy)


# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('动态创建可拖动标签')
#
#         self.layout = QVBoxLayout()
#
#         self.add_button = QPushButton('添加标签')
#         self.add_button.clicked.connect(self.add_label)
#         self.layout.addWidget(self.add_button)
#
#         self.setLayout(self.layout)
#
#         self.setGeometry(300, 300, 300, 200)
#         self.show()
#
#     def add_label(self):
#         new_label = DraggableLabel('拖动我')
#         self.layout.addWidget(new_label)
#         self.update()


def add_label(self, color, height, width):
    new_label = DraggableLabel()
    new_label.resize(width, height)
    new_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    new_label.setStyleSheet("background-color: " + color + ";color:" + color + ";border: 2px inset black;")
    new_label.h = height
    new_label.w = width
    self.layout.addWidget(new_label)
    # new_label.setFixedSize(width, height)
    # new_label.setFixedHeight(height)
    # new_label.setFixedWidth(width)
    new_label.setVisible(True)
    new_label.resize(width, height)
    # self.update()
    global _self, labels
    _self = self
    # for i in range(len(self.layout)):
    #     item = self.layout.itemAt(i)
    #     widget = item.widget()
    #     if widget:
    #         # widget.init()
    #         widget.move(widget.xx, widget.yy)
    # _self.lineEdit_5.setText(str(width))
    # _self.lineEdit_6.setText(str(height))
    # new_label.init(width, height)


def rotate_label(self):
    if _self_label is not None:
        if _self_label.image_flag == 0:
            height = _self_label.size().height()
            width = _self_label.size().width()
            _self_label.setVisible(True)
            _self_label.w = height
            _self_label.h = width
            # _self_label.setFixedSize(height, width)
            # _self_label.setFixedHeight(width)
            # _self_label.setFixedWidth(height)
            _self_label.resize(height, width)
            _self_label.rotate_flag = (_self_label.rotate_flag + 1) % 2
            init_all(self)
        else:
            rotate_label_image()
            init_all(self)


def rotate_label_image():
    transform = QTransform()
    transform.rotate(90)
    pix = _self_label.pixmap()
    # _self_label.setVisible(False)
    rotated_pix = pix.transformed(transform)
    _self_label.setPixmap(rotated_pix)
    _self_label.setVisible(True)


def change_label_size():
    if _self_label is not None:
        width = _self.lineEdit_5.text()
        height = _self.lineEdit_6.text()
        _self_label.resize(int(width), int(height))
        # _self_label.setFixedSize(int(width), int(height))
        #
        # _self_label.setFixedHeight(int(height))
        # _self_label.setFixedWidth(int(width))
        _self_label.w = int(width)
        _self_label.h = int(height)


#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())


# 添加几种图标的label
def add_image_label(self, image):
    # image = 'logo.png'
    pix = QPixmap(image)

    new_label = DraggableLabel()
    new_label.setPixmap(pix)
    new_label.setFixedSize(60, 60)
    new_label.setStyleSheet("border: 0px; background-color: transparent;")
    new_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.layout.addWidget(new_label)
    new_label.setVisible(True)
    new_label.setScaledContents(True)
    # new_label.resize(60, 60)
    new_label.image = image
    new_label.image_flag = 1
    new_label.h = 60
    new_label.w = 60
    global _self
    _self = self


def init_background(self):
    frame = self.frame_Mapping

    def newpaintEvent(self, frame):
        def paintEvent(event):
            painter = QPainter(frame)
            painter.setRenderHint(QPainter.Antialiasing, True)

            # 设置网格线的颜色和宽度
            pen = QPen(Qt.lightGray, 1, Qt.SolidLine)

            # 绘制网格线
            grid_size = 10  # 网格大小为 10px
            for x in range(0, frame.width(), grid_size):
                painter.setPen(pen)
                painter.drawLine(x, 0, x, frame.height())

            for y in range(0, frame.height(), grid_size):
                painter.setPen(pen)
                painter.drawLine(0, y, frame.width(), y)

        return paintEvent

    frame.paintEvent = newpaintEvent(self, frame)


def init_all(self):
    for i in range(len(self.layout)):
        item = self.layout.itemAt(i)
        widget = item.widget()
        if widget:
            # widget.init()
            # print(widget.x(), widget.y())
            # current_geometry = widget.geometry()
            # widget.setVisible(True)
            widget.show()
            widget.move(widget.xx, widget.yy)
            widget.resize(widget.w,
                          widget.h)

            widget.setGeometry(widget.xx, widget.yy, widget.w,
                               widget.h)
            # current_geometry = widget.geometry()
            # print(current_geometry)
            # print(widget.x(), widget.y())
            self.update()


def delete_pipe(self):
    try:
        _self_label.deleteLater()
        global _self
        _self = self
        QTimer.singleShot(10, on_timer_timeout)

    except Exception as e:
        print(e)


def on_timer_timeout():
    init_all(_self)
