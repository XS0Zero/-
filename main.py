import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog
from Gui.Login import Ui_MainWindow as Login_window
from Gui.MainWindow import Ui_MainWindow as MainWindow
from Gui.NewWork import NewWork_Dialog
from ctrl.Jieliu_slot import on_compute_button_clicked

from ctrl.Login_slot import getUserInfo, on_login_button_clicked, on_exit_button_clicked
from ctrl.menu_slot import change_page


class Login_window(QMainWindow, Login_window):
    def __init__(self):
        getUserInfo()
        super(Login_window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录窗口")
        self.pushButton.clicked.connect(lambda: on_login_button_clicked(self, window, Main_window))
        self.pushButton_2.clicked.connect(on_exit_button_clicked)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            on_login_button_clicked(self, window, Main_window)


class MainWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("主窗口")
        self.pushButton.clicked.connect(lambda: on_compute_button_clicked(self))
        # self.action1.triggered.connect(newWork(self))
        self.actionj.triggered.connect(lambda: change_page(self, 0))
        self.actionp.triggered.connect(lambda: change_page(self, 1))
        self.setinit()

    def setinit(self):
        self.QgEdit.setText("300000")
        self.QlEdit.setText("300")
        self.rEdit.setText("0.62")
        self.P1Edit.setText("58.3")
        self.PflqEdit.setText("10")
        self.T1Edit.setText("54.85")
        self.DEdit.setText("0.062")
        self.nEdit.setText("10")
        self.LLEdit.setText("10,10,5")
        self.LL1Edit.setText("1,2,2")
        self.LL2Edit.setText("1,2,2")
        self.LL3Edit.setText("1,2,2")


# class NewWork_Dialog(QDialog, NewWork_Dialog):
#     def __init__(self):
#         super(NewWork_Dialog, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle("新建工程")


def newWork():
    print("NewWork")
    dialog = NewWork_Dialog()
    # dialog.setWindowTitle("新建工程")
    # dialog.setWindowModality(Qt.ApplicationModal)
    # dialog.exec_()
    dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = Login_window()
    window = MainWindow()
    Main_window = MainWindow()
    window.show()
    sys.exit(app.exec_())
