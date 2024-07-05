import sys
from PyQt5.QtCore import Qt, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: white; padding: 10px; border: 1px solid black;")

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - self.pos())
            drag.exec_(Qt.MoveAction)

class DragDropWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.label1 = DraggableLabel("拖拽我")
        self.label2 = DraggableLabel("拖拽我")

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            pos = event.pos()
            self.label1.move(pos)
            self.label2.move(pos)
            event.acceptProposedAction()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DragDropWidget()
    widget.setWindowTitle("拖拽组件拼装界面")
    widget.show()
    sys.exit(app.exec_())
