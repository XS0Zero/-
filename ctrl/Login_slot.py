import os
import sys

import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

array = []
def getUserInfo():
    print("当前工作目录：%s" % os.getcwd())
    data = pd.read_csv(r'resource/user.csv', sep=',', header=0)
    global array
    array = data.values[0::, 0::]  # 读取全部行，全部列
    # print(array)


def on_login_button_clicked(self,window,Main_window):
    # print("登录按钮被点击了")
    # 在这里添加登录逻辑
    if get_input_text(self.lineEdit.text(), self.lineEdit_2.text()):
        print("登录成功")

        ico_path = os.path.join(os.path.dirname(__file__), 'resource/logo.ico')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ico_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Main_window.setWindowIcon(icon)
        Main_window.show()
        window.hide()

    else:
        print("登录失败")


def on_exit_button_clicked():
    print("退出按钮被点击了")
    # 在这里添加退出逻辑，例如关闭窗口或退出程序
    sys.exit()


def get_input_text(username, password):
    # username = username.text()
    # password = password.text()
    # print("用户名:", username, "密码:", password)
    return check_password(username, password)

def check_password(n, p):
    for i in range(len(array)):
        if array[i][0] == n and array[i][1] == p:
            return True
    return False


