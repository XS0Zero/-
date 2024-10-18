import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform, QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame, QLayout, QSizePolicy

# import main

_self = None
_self_label = None
label_dict = {}
label_count = 0

class DraggableLabel(QLabel):
    w = 0
    h = 0
    image_flag = 0
    image = None

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAlignment(Qt.AlignCenter)
        self.endPoint = None

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
            self.endPoint = self.pos()
            global _self_label
            _self_label = self

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("mouseRelease")
            print(self.pos())
            curr_pos_x = self.pos().x()
            curr_pos_y = self.pos().y()
            curr_rotate_angle = 0

            """
            搜索所有控件，找出离此最近的控件， 并判断控件的类型几控件的角度 再做处理
            """
            # if self.objectName() == "gudingdian":
            #     self.raise_()
            for key, curr_label in label_dict.items():
            #     if curr_label.objectName() == "gudingdian":
            #         print(1111111111111111111111)
            #         curr_label.raise_()
                if curr_label == self:
                    curr_rotate_angle = int(key.split("_")[1])
            if (abs(curr_pos_x - self.endPoint.x()) < 5 and abs(curr_pos_y - self.endPoint.y()) < 5):#判断是点击还是拖动
                pass

            else:
                if len(label_dict) >= 2:
                    for key, curr_label in label_dict.items():
                        label_x = curr_label.pos().x()
                        label_y = curr_label.pos().y()
                        curr_angle = int(key.split("_")[1])

                        if curr_label.objectName() == "pipeline":
                            if curr_label.width() > curr_label.height(): #管道为水平
                                if abs(label_x + curr_label.width() - curr_pos_x) < 40 and abs(label_y - curr_pos_y) < 40: #尾部
                                    if self.objectName() == "falan":
                                        if curr_rotate_angle == 0 or curr_rotate_angle == 180:
                                            self.move(label_x + curr_label.width()-self.width()/2+12, label_y - self.height()/2+4)
                                    elif self.objectName() == "wantou":
                                        if curr_rotate_angle == 90:
                                            self.move(label_x + curr_label.width()-self.width()/2+12, label_y - self.height()/2+3)
                                        elif curr_rotate_angle == 180:
                                            self.move(label_x + curr_label.width() - self.width() / 2 + 12,
                                                      label_y - self.height() / 2-3)
                                    elif self.objectName() == "jingkou":
                                        if curr_rotate_angle == 0:
                                            self.move(label_x + curr_label.width()-self.width()/2+12, label_y - self.height()+15)
                                    else:
                                        pass

                                elif abs(label_x - curr_pos_x) < 40 and abs(label_y - curr_pos_y) < 40:#头部
                                    if self.objectName() == "falan":
                                        if curr_rotate_angle == 0 or curr_rotate_angle == 180:
                                            self.move(label_x-self.width()+10, label_y - self.height()/2+4)
                                    elif self.objectName() == "wantou":
                                        if curr_rotate_angle == 0:
                                            self.move(label_x-self.width()/2-10, label_y - self.height()/2+8)
                                        elif curr_rotate_angle == 270:
                                            self.move(label_x - self.width() / 2 - 10,
                                                      label_y - self.height() / 2+1)
                                    elif self.objectName() == "jingkou":
                                        if curr_rotate_angle == 0:
                                            self.move(label_x-self.width()/2-20, label_y - self.height()+14)

                                    else:
                                        pass
                            else: #管道为垂直
                                if abs(label_x - curr_pos_x) < 40 and abs(label_y + curr_label.height() - curr_pos_y) < 40:  # 尾部
                                    if self.objectName() == "falan":
                                        if curr_rotate_angle == 90 or curr_rotate_angle == 270:
                                            self.move(label_x-self.width()/2+3, label_y+ curr_label.height() - self.height()/2+8)
                                    elif self.objectName() == "wantou":
                                        if curr_rotate_angle == 180:
                                            self.move(label_x-self.width()/2+1, label_y+ curr_label.height() - self.height()/2+8)
                                        elif curr_rotate_angle == 270:
                                            self.move(label_x - self.width() / 2 + 9,label_y + curr_label.height() - self.height() / 2 + 8)

                                    else:
                                        pass

                                elif abs(label_x - curr_pos_x) < 40 and abs(label_y - curr_pos_y) < 40:  # 头部
                                    if self.objectName() == "falan":
                                        if curr_rotate_angle == 90 or curr_rotate_angle == 270:
                                            self.move(label_x - self.width() / 2 + 3, label_y - self.height()+8)
                                    elif self.objectName() == "wantou":
                                        if curr_rotate_angle == 0:
                                            self.move(label_x - self.width() / 2 + 4,
                                                      label_y - self.height()+20)
                                        elif curr_rotate_angle == 90:
                                            self.move(label_x - self.width() / 2-4,
                                                      label_y  - self.height() / 2-7 )

                                    else:
                                        pass
                        elif curr_label.objectName() == "jingkou":
                            if abs(label_x + curr_label.width() - curr_pos_x) < 40 and abs(
                                    label_y - curr_pos_y) < 40:
                                if self.objectName() == "pipeline":
                                    if curr_label.width() > curr_label.height():
                                        self.move(label_x + curr_label.width() - 15, label_y + curr_label.height()-14)
                        elif curr_label.objectName() == "falan":
                            if abs(label_x + curr_label.width() - curr_pos_x) < 40 and abs(
                                    label_y - curr_pos_y) < 40:
                                print(curr_angle)
                                if curr_angle == 0 or curr_angle == 180:
                                    if self.objectName() == "pipeline":
                                        if self.width() > self.height():
                                            self.move(label_x+curr_label.width()-20, label_y+curr_label.height()/2-2)
                                else:
                                    if self.objectName() == "pipeline":
                                        if self.width() < self.height():
                                            self.move(label_x+37, label_y + curr_label.height()-10)

                        elif curr_label.objectName() == "wantou":
                            if abs(label_x + curr_label.width() - curr_pos_x) < 40 and abs(
                                    label_y - curr_pos_y) < 40:
                                print(curr_angle)
                                if curr_angle == 0:
                                    if self.objectName() == "pipeline":
                                        if self.width() > self.height():
                                            self.move(label_x + curr_label.width()/2+10, label_y + curr_label.height()/2-8)
                                        else:
                                            self.move(label_x + curr_label.width() / 2-4,
                                                      label_y + curr_label.height() / 2 + 8)
                                elif curr_angle == 90:
                                    if self.objectName() == "pipeline":
                                        if self.width() < self.height():
                                            self.move(label_x + curr_label.width() / 2+4 ,
                                                      label_y + curr_label.height() / 2+8)

                                elif curr_angle == 270:
                                    if self.objectName() == "pipeline":
                                        if self.width() > self.height():
                                            self.move(label_x + curr_label.width()/2+5, label_y + curr_label.height()/2-2)


                            else:
                                pass





    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset is not None:
            # self.move(self.pos() + event.pos())
            # self.offset = event.pos()
            # print("Label position when dragged:", self.pos())
            x, y = event.pos().x(), event.pos().y()
            offset_x, offset_y = self.offset.x(), self.offset.y()
            new_x, new_y = x - offset_x, y - offset_y

            # 将移动差值调整为25的整数倍
            # new_x = new_x - (new_x % 10)
            # new_y = new_y - (new_y % 10)

            self.move(self.x() + new_x, self.y() + new_y)

    def init(self, h, w):
        self.resize(h, w)
        global _self_label
        _self_label = self
        change_label_size()


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
    new_label = DraggableLabel(self.frame_Mapping)
    new_label.resize(width, height)
    new_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    new_label.setStyleSheet("background-color: " + color + ";color:" + color )#+ ";border: 2px inset #e04129;"
    new_label.setObjectName("pipeline")
    new_label.h = height*10
    new_label.w = width
    # self.layout.addWidget(new_label)
    new_label.setGeometry(900, 150, 50, 30)
    new_label.setFixedSize(width, height)
    new_label.lower()
    new_label.show()


    global label_count
    label_count += 1
    label_dict[f"{label_count}_0"] = new_label
    # label_list.append(new_label)

    self.update()
    global _self
    _self = self
    # _self.lineEdit_5.setText(str(width))
    # _self.lineEdit_6.setText(str(height))
    # new_label.init(width, height)




def delete_lable():
    """
    删除控件
    """
    global _self_label
    if _self_label is not None:
        # label_list.remove(_self_label)
        _self_label.deleteLater()
        for key, value in label_dict.items():
            if value == _self_label:
                del label_dict[key]
                _self_label = None
                return






def rotate_label():
    if _self_label is not None:
        if _self_label.image_flag == 0:
            height = _self_label.size().height()
            width = _self_label.size().width()
            _self_label.setFixedSize(height, width)
        else:
            """
            增加标记，判断位置
            """
            rotate_label_image()


def rotate_label_image():
    transform = QTransform()
    transform.rotate(90)
    pix = _self_label.pixmap()
    rotated_pix = pix.transformed(transform)
    _self_label.setPixmap(rotated_pix)
    for key, value in label_dict.items():
        if value == _self_label:
            old_id = key.split("_")[0]
            old_angle = key.split("_")[1]
            new_angle = int(old_angle) + 90
            if new_angle == 360:
                new_angle = 0
            # label_dict.update({old_id + "_" + str(new_angle): label_dict.pop(key)})
            label_dict[old_id + "_" + str(new_angle)] = label_dict[key]
            del label_dict[key]
            return



def change_label_size():
    if _self_label is not None:
        if _self_label.image_flag == 0:
            width = int(_self.lineEdit_5.text())
            if width > 300:
                width = 300 + width/10
            height = int(_self.lineEdit_6.text())/10
            if _self_label.height() > _self_label.width():#管道垂直

                _self_label.setFixedSize(height, width)
            else:
                _self_label.setFixedSize(width, height)
            if width > 300:
                _self_label.w = int((width-300)*10)
            else:
                _self_label.w = int(width)
            _self_label.h = int(height)*10
        else:
            width = _self.lineEdit_5.text()
            height = _self.lineEdit_6.text()
            _self_label.setFixedSize(int(width), int(height))
            _self_label.w = int(width)
            _self_label.h = int(height)


#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())


# 添加几种图标的label
def add_image_label(self, image, image_name):
    # image = 'logo.png'
    pix = QPixmap(image)
    # pix.scaled(20,20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    new_label = DraggableLabel(self.frame_Mapping)
    new_label.setPixmap(pix)
    new_label.setScaledContents(True)
    new_label.setObjectName(image_name)
    new_label.setStyleSheet("border: 0px; background-color: transparent;")
    new_label.image = image
    new_label.image_flag = 1
    new_label.h = 60
    new_label.w = 80
    new_label.setFixedHeight(60)
    new_label.setFixedWidth(80)
    new_label.setGeometry(900, 150, 50, 30)

    new_label.show()


    # lable_dict = {"1": new_label}
    # print(type(new_label))
    # print("-----------------------------------")
    # print(type(lable_dict["1"]))
    # label_list.append(new_label)
    global label_count
    label_count += 1
    label_dict[f"{label_count}_0"] = new_label
    self.update()
    global _self
    _self = self

def init_background(self):
    frame = self.frame_Mapping
    def newpaintEvent(self, frame):
        def paintEvent(event):
            painter = QPainter(frame)
            painter.setRenderHint(QPainter.Antialiasing, True)

            # 设置网格线的颜色和宽度
            # pen = QPen(Qt.lightGray , 1, Qt.SolidLine)

            # 绘制网格线
            # grid_size = 5  # 网格大小为 10px
            # for x in range(0, frame.width(), grid_size):
            #     painter.setPen(pen)
            #     painter.drawLine(x, 0, x, frame.height())
            #
            # for y in range(0, frame.height(), grid_size):
            #     painter.setPen(pen)
            #     painter.drawLine(0, y, frame.width(), y)

        return paintEvent

    frame.paintEvent = newpaintEvent(self,frame)