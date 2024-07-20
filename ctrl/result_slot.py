import numpy as np
import pandas as pd
import sys

sys.setrecursionlimit(2000)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QGraphicsScene, QGraphicsView
from matplotlib import pyplot as plt

from data import result_form
from utils.image_utils import base64_to_image


def init_result(self):
    # print(result_form.jieliu_result)
    # print(result_form.moudle3_result)
    # print(result_form.image_base64)
    # print(result_form.Project_inform)
    if result_form.Project_inform is not None:
        self.lineEdit_Project_inform1.setText(result_form.Project_inform[0])

        self.lineEdit_Project_inform2.setText(result_form.Project_inform[1])

        self.lineEdit_Project_inform3.setText(result_form.Project_inform[2])

        self.lineEdit_Project_inform4.setText(result_form.Project_inform[3])

    if result_form.jieliu_result is not None:
        result = result_form.jieliu_result
        self.d_label_3.setText(result[0])  # round(result[0],2)
        self.dd_label_3.setText(result[1])
        self.ddd_label_3.setText(result[2])
        self.T2_label_3.setText(result[3])
        self.T22_label_3.setText(result[4])
        self.T222_label_3.setText(result[5])
        self.P1jl_3.setText(result[6])
        self.P2jl_3.setText(result[7])
        self.P3jl_3.setText(result[8])
        self.P2_3.setText(result[9])
        self.P22_3.setText(result[10])
        self.P222_3.setText(result[11])
        self.Pctiz1_3.setText(result[12])
        self.Pctiz2_3.setText(result[13])
        self.Pctiz3_3.setText(result[14])
        self.Pctiz4_3.setText(result[15])
        self.Qd_3.setText(result[16])

    if result_form.moudle3_flag:

        df = result_form.moudle3_result
        # 获取行数和列数
        rows, cols = df.shape

        # 设置表格的行数和列数
        self.tableWidget_2.setRowCount(rows)
        self.tableWidget_2.setColumnCount(cols)

        # 读取数据并显示在表格中
        for i in range(rows):
            for j in range(cols):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    if result_form.image_base64:
        # 将base64编码的图像转换为QImage对象
        base64_to_image(result_form.image_base64, "mapping.png")
        # 将QImage对象转换为QPixmap对象
        # 创建一个graphicsScene对象
        self.graphics_scene = QGraphicsScene(self)

        # 将图片加载到graphicsScene中
        pixmap = QPixmap("mapping.png")
        self.graphics_scene.addPixmap(pixmap)

        # 将graphicsScene设置为graphicsView的场景
        self.graphicsView.setScene(self.graphics_scene)

        # 设置graphicsView的缩放模式
        self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    if result_form.Vc is not None:
        self.tableWidget_3.setRowCount(3)
        self.tableWidget_3.setColumnCount(3)

        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(str(round(result_form.Vc, 2))))
        self.tableWidget_3.setItem(0, 1, QTableWidgetItem(str(round(result_form.Ve, 2))))
        if result_form.Vc > result_form.Ve:
            if result_form.Vc - result_form.Ve > 80:
                self.tableWidget_3.setItem(0, 2, QTableWidgetItem("严重冲蚀"))
            else:
                if result_form.Vc - result_form.Ve > 30:
                    self.tableWidget_3.setItem(0, 2, QTableWidgetItem("中等冲蚀"))
                else:
                    self.tableWidget_3.setItem(0, 2, QTableWidgetItem("轻微冲蚀冲蚀"))
        else:
            self.tableWidget_3.setItem(0, 2, QTableWidgetItem("无冲蚀"))
    if result_form.Vcc is not None:
        self.tableWidget_3.setItem(1, 0, QTableWidgetItem(str(round(result_form.Vcc, 2))))
        self.tableWidget_3.setItem(1, 1, QTableWidgetItem(str(round(result_form.Vee, 2))))
        if result_form.Vcc > result_form.Vee:
            if result_form.Vcc - result_form.Vee > 80:
                self.tableWidget_3.setItem(1, 2, QTableWidgetItem("严重冲蚀"))
            else:
                if result_form.Vcc - result_form.Vee > 30:
                    self.tableWidget_3.setItem(1, 2, QTableWidgetItem("中等冲蚀"))
                else:
                    self.tableWidget_3.setItem(1, 2, QTableWidgetItem("轻微冲蚀冲蚀"))
        else:
            self.tableWidget_3.setItem(1, 2, QTableWidgetItem("无冲蚀"))
    if result_form.Vccc is not None:
        self.tableWidget_3.setItem(2, 0, QTableWidgetItem(str(round(result_form.Vccc, 2))))
        self.tableWidget_3.setItem(2, 1, QTableWidgetItem(str(round(result_form.Veee, 2))))
        if result_form.Vccc > result_form.Veee:
            if result_form.Vccc - result_form.Veee > 80:
                self.tableWidget_3.setItem(2, 2, QTableWidgetItem("严重冲蚀"))
            else:
                if result_form.Vccc - result_form.Veee > 30:
                    self.tableWidget_3.setItem(2, 2, QTableWidgetItem("中等冲蚀"))
                else:
                    self.tableWidget_3.setItem(2, 2, QTableWidgetItem("轻微冲蚀冲蚀"))
        else:
            self.tableWidget_3.setItem(2, 2, QTableWidgetItem("无冲蚀"))


def show_moulde3_image(self):
    if result_form.moudle3_flag:
        df = result_form.moudle3_result
        # 使用前两列数据生成图像
        plt.switch_backend('Qt5Agg')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(df.iloc[:, 0], df.iloc[:, 1])
        plt.xlabel('管长')
        plt.ylabel('振动位移')
        plt.title('振动位移随管长变化')
        plt.show()
    else:
        QMessageBox.information(self, "错误", "未有数据输入，请先输入数据并计算")
