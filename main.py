# import matlab.engine
# def matlab_function():
#
#     eng = matlab.engine.start_matlab()
#     eng.cd('matlab2')
#     eng.mainfunc(nargout=0)
#     print("Compute complete")
#     eng.quit()
#     return True
import os
import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDialog, QTableWidgetItem, QAction, QMessageBox
from qt_material import apply_stylesheet

import data.result_form
from Gui.Login import Ui_MainWindow as Login_window
from Gui.MainWindow import Ui_MainWindow as MainWindow
from Gui.NewWork import NewWork_Dialog
from ctrl.Jieliu_slot import on_compute_button_clicked

from ctrl.Login_slot import getUserInfo, on_login_button_clicked, on_exit_button_clicked
from ctrl.compute_slot import module3_compute, add_a, delete_a
from ctrl.menu_slot import change_page, save_project, load_project
from ctrl.mappint_slot import add_label, rotate_label, change_label_size, add_image_label
import pandas as pd

from ctrl.result_slot import init_result, show_moulde3_image
from data import result_form
from utils.image_utils import png_to_base64


class Login_window(QMainWindow, Login_window):
    def __init__(self):
        getUserInfo()
        super(Login_window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录")
        self.pushButton.clicked.connect(lambda: on_login_button_clicked(self, window, Main_window))
        self.pushButton_2.clicked.connect(on_exit_button_clicked)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return:
            on_login_button_clicked(self, window, Main_window)


class MainWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        _self = self
        self.setupUi(self)
        self.setWindowTitle("超高压地面测试流程综合分析软件")

        self.message = message(self)


        self.pushButton.clicked.connect(lambda: on_compute_button_clicked(self))
        # self.menu_2.triggered.connect(lambda: change_page(self, 5))
        # self.menu_2.addAction(lambda: change_page(self, 5))
        self.menu_2_action = QAction()
        self.menu_2_action.setCheckable(False)
        self.menu_2_action.setObjectName('menu_2_action')
        self.menu_2_action.triggered.connect(lambda: change_page(_self, 4))
        self.menu_2_action.setText('新建工程')
        self.menubar.addAction(self.menu_2_action)

        self.menu_3_action = QAction()
        self.menu_3_action.setCheckable(False)
        self.menu_3_action.setObjectName('menu_3_action')
        self.menu_3_action.triggered.connect(lambda: save_project(_self))
        self.menu_3_action.setText('保存工程')
        self.menubar.addAction(self.menu_3_action)

        self.menu_4_action = QAction()
        self.menu_4_action.setCheckable(False)
        self.menu_4_action.setObjectName('menu_2_action')
        self.menu_4_action.triggered.connect(lambda: load_project(_self))
        self.menu_4_action.setText('打开工程')
        self.menubar.addAction(self.menu_4_action)

        self.menu_5_action = QAction()
        self.menu_5_action.setCheckable(False)
        self.menu_5_action.setObjectName('menu_2_action')
        self.menu_5_action.triggered.connect(self.close)
        self.menu_5_action.setText('退出')
        self.menubar.addAction(self.menu_5_action)

        self.actionj.triggered.connect(lambda: change_page(self, 1))
        self.actionp.triggered.connect(lambda: change_page(self, 2))
        self.actiona.triggered.connect(lambda: change_page(self, 3))
        self.actions.triggered.connect(self.show_result)

        # self.setinit()

        self.pushButton_3.clicked.connect(lambda: module3_compute(self))
        self.pushButton_add.clicked.connect(lambda: add_a(self))
        self.pushButton_delete.clicked.connect(lambda: delete_a(self))
        self.buttonBox.accepted.connect(self.startProject)
        self.addpipe2.clicked.connect(lambda: add_label(self, "#4ce500", 25, 100))
        self.addpipe3.clicked.connect(lambda: add_label(self, "#f3f300", 25, 100))
        self.addpipe1.clicked.connect(lambda: add_label(self, "#00aaff", 25, 100))
        self.addpipe1_2.clicked.connect(lambda: add_label(self, "#bfbfbf", 30, 30))
        self.addpipe1_3.clicked.connect(lambda: add_image_label(self, "resource/falan.png"))
        self.addpipe1_4.clicked.connect(lambda: add_image_label(self, "resource/zhijiaojietou.png"))
        self.addpipe1_5.clicked.connect(lambda: add_image_label(self, "resource/gudingdian.png"))
        self.addpipe1_6.clicked.connect(lambda: add_image_label(self, "resource/zhenfa.png"))

        self.pushButton_2.clicked.connect(self.saveimage)
        self.pushButton_5.clicked.connect(lambda: rotate_label())
        self.pushButton_4.clicked.connect(lambda: change_label_size())

        self.pushButton_7.clicked.connect(lambda: show_moulde3_image(self))

    def box(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)

    def menu_2_triggered(self):
        print("menu_2 triggered")
        change_page(self, 5)

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

        self.lineEdit_a1.setText("30")
        self.lineEdit_a2.setText("54")
        self.lineEdit_a3.setText("7.3")
        self.lineEdit_a4.setText("50")
        self.lineEdit_a5.setText("0.06")
        self.lineEdit_a6.setText("0.08")
        self.lineEdit_a7.setText("15.4")

        # 弃置滚动栏样式
        # self.addScrollBarStyle()

    def addScrollBarStyle(self):
        # 1.新建一个名字叫textEdit_send_sbar的滚动条
        self.textEdit_send_sbar = QtWidgets.QScrollBar()

        # 2.给这个滚动条添加属性
        self.textEdit_send_sbar.setStyleSheet("""
             QScrollBar:vertical {
                  border-width: 0px;
                  border: none;
                  background:rgba(64, 65, 79, 0);
                  width:12px;
                  margin: 0px 0px 0px 0px;
              }
              QScrollBar::handle:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0 #aaaaff, stop: 0.5 #aaaaff, stop:1 #aaaaff);
                  min-height: 20px;
                  max-height: 20px;
                  margin: 0 0px 0 0px;
                  border-radius: 6px;
              }
              QScrollBar::add-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0px;
                  border: none;
                  subcontrol-position: bottom;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-line:vertical {
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                  stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
                  height: 0 px;
                  border: none;
                  subcontrol-position: top;
                  subcontrol-origin: margin;
              }
              QScrollBar::sub-page:vertical {
              background: rgba(64, 65, 79, 0);
              }

              QScrollBar::add-page:vertical {
              background: rgba(64, 65, 79, 0);
              }
              """)

        # 3.把这个textEdit_send_sbar当作属性附加到textEdit控件上
        self.scrollArea.setVerticalScrollBar(self.textEdit_send_sbar)

    def saveimage(self):
        self = self.frame_Mapping
        pixmap = QApplication.primaryScreen().grabWindow(self.winId())
        pixmap.save('mapping.png', 'png')
        result_form.image_base64 = png_to_base64('mapping.png')

    def startProject(self):

        try:
            inform = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text()]
            print(inform)
            flag = 1
            for i in inform:
                if i == '':
                    QMessageBox.information(self, "提示", "请输入完整信息")
                    flag = 0
                    break
            if flag == 1:
                data.result_form.Project_inform = inform
                change_page(self, 1)
        except Exception as e:
            QMessageBox.information(self, "提示", "请输入正确信息")

    def show_result(self):
        init_result(self)
        change_page(self, 0)


# class NewWork_Dialog(QDialog, NewWork_Dialog):
#     def __init__(self):
#         super(NewWork_Dialog, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle("新建工程")


# def newWork():
#     print("NewWork")
#     dialog = NewWork_Dialog()
#     # dialog.setWindowTitle("新建工程")
#     # dialog.setWindowModality(Qt.ApplicationModal)
#     # dialog.exec_()
#     dialog.show()


class message(QThread):
    signal = pyqtSignal()

    def __init__(self, Window):
        super(message, self).__init__()
        self.window = Window

    def run(self):
        self.signal.emit()


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Login_window()
    # window = MainWindow()
    Main_window = MainWindow()
    ico_path = os.path.join(os.path.dirname(__file__), 'resource/logo.ico')
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(ico_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    window.setWindowIcon(icon)
    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec_())
