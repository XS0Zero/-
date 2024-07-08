import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame, QLayout


class DraggableLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: white; padding: 10px; border: 1px solid black;")
        self.setFixedHeight(20)  # 设置标签的高度为5px
        self.setFixedWidth(150)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)
            self.offset = event.pos()


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


def add_label(self):
    new_label = DraggableLabel('拖动我')
    self.layout.addWidget(new_label)
    self.update()

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())
