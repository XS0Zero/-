import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QFileDialog

from data import result_form


def change_page(self, n):
    print("切换页面至", n)
    self.stackedWidget.setCurrentIndex(n)


def save_project(self):
    cwd = os.getcwd()
    fileName_save = QFileDialog.getSaveFileName(self,
                                                "文件保存",
                                                cwd,  # 起始路径
                                                "保存工程文件 (*.csv)")
    print(fileName_save)
    if fileName_save[0] != "":
        result_form.save_project(self, fileName_save[0])


def load_project(self):
    cwd = os.getcwd()
    fileName_save = QFileDialog.getOpenFileName(self, "文件打开",
                                                cwd,  # 起始路径
                                                "保存工程文件 (*.csv)")
    print(fileName_save)

    if fileName_save[0] != "":
        result_form.open_project(self, fileName_save[0])
