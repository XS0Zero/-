# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login1.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets


def check_password(n, p):
    for i in range(len(array)):
        if array[i][0] == n and array[i][1] == p:
            return True
    return False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(250, 60, 321, 301))
        self.widget.setObjectName("widget")
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setGeometry(QtCore.QRect(30, 10, 271, 201))
        self.listWidget.setStyleSheet("background-color: rgb(216, 216, 216,180);\n"
                                      "border-radius:25px;")
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 50, 191, 31))
        self.lineEdit.setStyleSheet("border-radius:5px")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 120, 191, 31))
        self.lineEdit_2.setStyleSheet("border-radius:5px")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(60, 240, 81, 31))
        self.pushButton.setStyleSheet("#pushButton{\n"
                                      "    \n"
                                      "    background-color: rgb(255, 255, 255);\n"
                                      "    color: rgb(0, 0, 0);\n"
                                      "    border:1px solid rgb(0,0,0);\n"
                                      "    border-radius:8px;\n"
                                      "}\n"
                                      "#pushButton:hover{\n"
                                      "    \n"
                                      "    background-color: rgb(158, 158, 158);\n"
                                      "    \n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "}\n"
                                      "#pushButton:pressed{\n"
                                      "    padding-top:5px;\n"
                                      "    padding-left:5px;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 240, 81, 31))
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
                                        "    \n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "    color: rgb(0, 0, 0);\n"
                                        "    border:1px solid rgb(0,0,0);\n"
                                        "    border-radius:8px;\n"
                                        "}\n"
                                        "#pushButton_2:hover{\n"
                                        "    \n"
                                        "    background-color: rgb(158, 158, 158);\n"
                                        "    \n"
                                        "    color: rgb(255, 255, 255);\n"
                                        "}\n"
                                        "#pushButton_2:pressed{\n"
                                        "    padding-top:5px;\n"
                                        "    padding-left:5px;\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 400))
        self.label.setMaximumSize(QtCore.QSize(600, 400))
        self.label.setStyleSheet("opacity:0.5;\n"
                                 "background-color: rgb(255, 255, 255,0);\n"
                                 "border-image: url(:/images/resource/images/2.png);\n"
                                 "border-radius:15px;\n"
                                 "")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.raise_()
        self.widget.raise_()
        # MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "用户名："))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "密码："))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))
        self.pushButton.clicked.connect(self.on_login_button_clicked)
        self.pushButton_2.clicked.connect(self.on_exit_button_clicked)

        self.label.setProperty("setWindowOpacity", _translate("MainWindow", "0.7"))

    def on_login_button_clicked(self):
        print("登录按钮被点击了")
        # 在这里添加登录逻辑
        if self.get_input_text():
            print("登录成功")
        else:
            print("登录失败")

    def on_exit_button_clicked(self):
        print("退出按钮被点击了")
        # 在这里添加退出逻辑，例如关闭窗口或退出程序
        sys.exit()

    def get_input_text(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        print("用户名:", username, "密码:", password)
        return check_password(username, password)


import resource_rc

if __name__ == "__main__":
    import sys
    import os

    print("当前工作目录：%s" % os.getcwd())
    data = pd.read_csv(r'../resource/user.csv', sep=',', header=0)
    array = data.values[0::, 0::]  # 读取全部行，全部列

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())


