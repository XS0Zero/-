import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from Gui.Login import Ui_MainWindow as Login_window
from Gui.MainWindow import Ui_MainWindow as MainWindow
from ctrl.Jieliu_slot import on_compute_button_clicked

from ctrl.Login_slot import getUserInfo, on_login_button_clicked, on_exit_button_clicked


class Login_window(QMainWindow, Login_window):
    def __init__(self):
        getUserInfo()
        super(Login_window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录窗口")
        self.pushButton.clicked.connect(lambda: on_login_button_clicked(self,window,Main_window))
        self.pushButton_2.clicked.connect(on_exit_button_clicked)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            on_login_button_clicked(self,window,Main_window)


class MainWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("主窗口")
        self.pushButton.clicked.connect(lambda: on_compute_button_clicked(self))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login_window()
    Main_window = MainWindow()
    window.show()
    sys.exit(app.exec_())
