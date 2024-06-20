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

        # 计算结果初始化

        # Qg = 300000  # 气产量m^3/d
        # Ql = 300  # 液体产量m^3/d
        # r = 0.62  # 天然气相对密度
        # P1 = 58.3  # 井口压力MPa
        # Pflq = 10  # 分离器处压力MPa
        # T1 = 54.85  # 节流前温度，℃
        # R = 8.314  # 气体常数
        # k = 1.2917  # 比热容比
        # Tci = 190.69  # 临界温度，K
        # Pci = 4.64  # 临界压力,Pa
        # D = 0.062  # 管径,m
        # A = math.pi * D ** 2 / 4  # 管截面积
        # n = 10  # 弯头总个数

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = Login_window()
    window = MainWindow()
    Main_window = MainWindow()
    window.show()
    sys.exit(app.exec_())
