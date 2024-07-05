import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget


def change_page(self, n):
    print("切换页面至",n)
    self.stackedWidget.setCurrentIndex(n)
