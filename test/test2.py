from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication


class Button(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(100, 100)

        self.pos1 = 0  # 用于拖动时的鼠标位置初始值

    def mousePressEvent(self, QMouseEvent):
        self.pos1 = QMouseEvent.screenPos()

    def mouseReleaseEvent(self, QMouseEvent) -> None:
        fx, fy = self.frameGeometry().x(), self.frameGeometry().y()  # 相对父控件坐标
        tx_index, ty_index = fx // 100 if fx > 99 else 0, fy // 100 if fy > 99 else 0
        # 移动到网格上
        self.mymove(tx_index, ty_index)

    def mouseMoveEvent(self, QMouseEvent):
        pos2 = QMouseEvent.screenPos()
        tx = int(self.frameGeometry().x() + pos2.x() - self.pos1.x())
        ty = int(self.frameGeometry().y() + pos2.y() - self.pos1.y())
        self.move(tx, ty)
        self.pos1 = pos2

    def mymove(self, tx_index, ty_index):
        self.move(tx_index * 100, ty_index * 100)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('按钮测试')
        self.resize(500, 500)

        self.btn = Button(self)
        self.btn.setText('ABCD')

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
