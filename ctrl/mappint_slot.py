import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame, QLayout

# import main

_self = None
_self_label = None


class DraggableLabel(QLabel):
    w = 0
    h = 0
    image_flag = 0
    image = None

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            print("Label position when clicked:", self.pos())
            width = self.size().width()
            height = self.size().height()

            print("Label width:", width)
            print("Label height:", height)
            _self.lineEdit_5.setText(str(self.w))
            _self.lineEdit_6.setText(str(self.h))
            global _self_label
            _self_label = self

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("mouseRelease")
            print(self.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset is not None:
            self.move(self.pos() + event.pos())
            self.offset = event.pos()
            # print("Label position when dragged:", self.pos())


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
    new_label.setStyleSheet("background-color: " + color + ";color:" + color + ";border: 2px inset black;")
    new_label.h = height
    new_label.w = width
    new_label.setFixedHeight(height)
    new_label.setFixedWidth(width)
    self.layout.addWidget(new_label)
    self.update()
    global _self
    _self = self


def rotate_label():
    if _self_label is not None:
        if _self_label.image_flag == 0:
            height = _self_label.size().height()
            width = _self_label.size().width()
            _self_label.setFixedHeight(width)
            _self_label.setFixedWidth(height)
        else:
            rotate_label_image()


def rotate_label_image():
    transform = QTransform()
    transform.rotate(90)
    pix = _self_label.pixmap()
    rotated_pix = pix.transformed(transform)
    _self_label.setPixmap(rotated_pix)


def change_label_size():
    if _self_label is not None:
        width = _self.lineEdit_5.text()
        height = _self.lineEdit_6.text()
        _self_label.setFixedHeight(int(height))
        _self_label.setFixedWidth(int(width))
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
    new_label.setScaledContents(True)
    new_label.setStyleSheet("border: 0px")
    new_label.image = image
    new_label.image_flag = 1
    new_label.h = 35
    new_label.w = 35
    new_label.setFixedHeight(35)
    new_label.setFixedWidth(35)
    self.layout.addWidget(new_label)
    self.update()
    global _self
    _self = self
