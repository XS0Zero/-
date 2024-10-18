from Gui.Login import Ui_MainWindow as Login_window
from MainWindow import Ui_MainWindow as MainWindow

from PyQt5 import QtCore, QtWidgets
import sys
class MainWindow:
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)




class Login_window:
    def __init__(self):
        super(Login_window, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = Login_window()
    a.show()
    b = MainWindow()
    # button是你定义的按钮
    a.goButton.clicked.connect(
        lambda: {a.close(), b.show()}
    )
    sys.exit(app.exec_())
