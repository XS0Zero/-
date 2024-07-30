import math

import numpy as np
import pandas as pd
import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

sys.setrecursionlimit(2000)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QGraphicsScene, QGraphicsView
from matplotlib import pyplot as plt

from data import result_form
from utils.image_utils import base64_to_image


def init_result(self):
    try:
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
            # self.P2_3.setText(result[9])
            # self.P22_3.setText(result[10])
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

        if result_form.image_base64 is not None:
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

        try:
            result_form.Vc = float(result_form.Vc)
        except ValueError:
            result_form.Vc = 0
        try:
            result_form.Vcc = float(result_form.Vcc)
        except ValueError:
            result_form.Vcc = 0
        try:
            result_form.Vccc = float(result_form.Vccc)
        except ValueError:
            result_form.Vccc = 0

        if result_form.Vc is not None and not math.isnan(result_form.Vc):
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
        if result_form.Vcc is not None and not math.isnan(result_form.Vcc):
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
        if result_form.Vccc is not None and not math.isnan(result_form.Vccc):
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
        str1 = ''
        try:
            if result_form.G1 != 0:
                str1 += f"一级水合物抑制剂：{round(result_form.G1, 2)}kg/d"
            if result_form.G2 != 0:
                str1 += f"\n二级水合物抑制剂：{round(result_form.G2, 2)}kg/d"
            if result_form.G3 != 0:
                str1 += f"\n三级水合物抑制剂：{round(result_form.G3, 2)}kg/d"
        except TypeError:
            pass
        self.label_100.setText(str1)
    except Exception as e:
        QMessageBox.information(self, "错误", str(e))

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

def show_moulde1_image(self):
    try:
        if result_form.P2 is not None:
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
            plt.rcParams['axes.unicode_minus'] = False
            F1 = MyFigure(width=5, height=4, dpi=100)
            F1.axes1 = F1.fig.add_subplot(111)
            F1.axes1.plot(result_form.Px1[0], result_form.Tx1[0], 'r')
            # F1.axes1.plot(result_form.Px1[1], result_form.Tx1[1], 'r')
            # F1.axes1.plot(result_form.Px1[2], result_form.Tx1[2], 'r')
            F1.axes1.set_xlabel('压力 (MPa)', fontsize=11)
            F1.axes1.set_ylabel('温度 (℃)', fontsize=11)
            F1.axes1.set_title('水合物相平衡曲线')
            F1.axes1.plot(result_form.P2, result_form.T2, color='blue', marker='.', markersize=16)
            F1.axes1.text(result_form.P2, result_form.T2, '一级节流')
            result_form.Pflq = float(result_form.Pflq)
            if result_form.P2 > result_form.Pflq:
                F1.axes1.plot(result_form.P22, result_form.T22, color='red', marker='<', markersize=8)
                F1.axes1.text(result_form.P22, result_form.T22, '二级节流')
                if result_form.P22 > result_form.Pflq:
                    F1.axes1.plot(result_form.P222, result_form.T222, color='green', marker='*', markersize=8)
                    F1.axes1.text(result_form.P222, result_form.T222, '三级节流')

            width, height = self.graphicsView_2.width(), self.graphicsView_2.height()
            F1.resize(width, height)
            self.scene = QGraphicsScene()  # 创建一个场景
            self.scene.addWidget(F1)  # 将图形元素添加到场景中
            self.graphicsView_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.graphicsView_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.graphicsView_2.setScene(self.scene)  # 将创建添加到图形视图显示窗口
        else:
            QMessageBox.information(self, "错误", "未有数据输入，请先输入数据并计算")
    except Exception as e:
        QMessageBox.information(self, "错误", str(e))


# 重写一个matplotlib图像绘制类
class MyFigure(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        # 1、创建一个绘制窗口Figure对象
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 2、在父类中激活Figure窗口,同时继承父类属性
        super(MyFigure, self).__init__(self.fig)

    # 这里就是绘制图像、示例
    def plotSin(self, x, y):
        self.axes0 = self.fig.add_subplot(111)
        self.axes0.plot(x, y)