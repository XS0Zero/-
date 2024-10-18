import os
import subprocess
import time

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QGraphicsScene, QApplication
from matplotlib import pyplot as plt
from pandas.errors import EmptyDataError

from ctrl.result_slot import MyFigure
from data import result_form

saved_data = []


def add_a(self):
    global saved_data
    try:
        data = self.lineEdit_8.text()
        saved_data.append(float(data))
    except ValueError:
        print("输入错误")
        return None
    self.lineEdit_8.clear()
    self.label_75.setText(str(saved_data))


def delete_a(self):
    global saved_data
    try:
        saved_data.pop()
    except IndexError:
        print("没有数据可以删除")
        return None
    self.label_75.setText(str(saved_data))


def module3_compute(self):
    print("模块三开始计算")
    print("当前工作目录：%s" % os.getcwd())
    try:
        filename = '输入数据.csv'

        if os.path.exists(filename):
            df = pd.DataFrame()
            df.to_csv(filename, index=False)
        inputdata = pd.read_csv(r'输入数据.csv', sep=',', header=None)
    except EmptyDataError:
        # inputdata = pd.DataFrame(index=range(8), columns=range(6))
        inputdata = pd.DataFrame(index=range(8), columns=range(len(saved_data)))
    print(inputdata)
    print(inputdata.iloc[:, 0])

    def message():
        self.message.signal.connect(lambda: self.box("提示", "计算中，请稍后..."))
        self.message.start()

    def check_input(input_value):
        try:
            float(input_value)
            return True
        except ValueError:
            return False

    data = [0] * 7
    flag = 0
    try:
        for i in range(7):
            data[i] = getattr(self, f'lineEdit_a{i + 1}').text()
            if not check_input(data[i]):
                print("存在错误输入参数")
                QMessageBox.information(self, "提示", "存在错误输入参数")
                flag = 1
                break
        index = 0
        for i in saved_data:
            if not check_input(i):
                print("存在错误输入参数")
                QMessageBox.information(self, "提示", "存在错误输入参数")
                flag = 1
                break
            print(i)
            inputdata.iloc[7, index] = float(i)
            index += 1
    except Exception as e:
        print(e)
        QMessageBox.information(self, "错误", str(e))

    result_form.moudle3_inform = data
    result_form.moudle3_inform_2 = saved_data

    if flag == 0:
        for i in range(7):
            inputdata.iloc[i, 0] = float(data[i])

        inputdata.to_csv(r'输入数据.csv', index=False, header=False)
        filename = '振动位移随管长变化.csv'

        if os.path.exists(filename):
            df = pd.DataFrame()
            df.to_csv(filename, index=False)
        print(inputdata)
        # self.msg = QMessageBox()
        # # 设置非模态
        # self.msg.setWindowModality(Qt.NonModal)
        # # 设置弹窗标题和内容
        # self.msg.setWindowTitle('提示')
        # self.msg.setText('计算中，请稍后...')
        # # 设置弹窗的按钮为OK，StandardButtons采用位标记，可以用与运算添加其他想要的按钮
        # self.msg.setStandardButtons(QMessageBox.Ok)
        # # 显示窗口
        # self.msg.show()
        # time.sleep(1)
        print("开始调用matlab函数")
        self.msg = QMessageBox()
        # 设置非模态
        self.msg.setWindowModality(Qt.NonModal)
        # 设置弹窗标题和内容
        self.msg.setWindowTitle('提示')
        self.msg.setText('正在计算中')
        self.msg.setStandardButtons(QMessageBox.Ok)
        # 显示窗口
        self.msg.show()
        QApplication.processEvents()
        # message()
        # QMessageBox.information(self, "提示", "计算中，请稍后...")
        try:
            myPopenObj = subprocess.Popen("matlab2/test.exe")
            try:
                myPopenObj.wait(timeout=1200)
            except Exception as e:
                print("===== process timeout ======")
                print(e)
                myPopenObj.kill()
        except Exception as e:
            QMessageBox.information(self, "错误", str(e))
        print("模块三计算完成")

        self.msg.accept()
        try:
            df = pd.read_csv('振动位移随管长变化.csv')
            result_form.moudle3_flag = True
            QMessageBox.information(self, "提示", "模块三计算完成")
            result_form.moudle3_result = df
            # 获取行数和列数
            rows, cols = df.shape

            # 设置表格的行数和列数
            self.tableWidget.setRowCount(rows)
            self.tableWidget.setColumnCount(cols)

            # 读取数据并显示在表格中
            for i in range(rows):
                for j in range(cols):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

            # 使用前两列数据生成图像
            # plt.switch_backend('Qt5Agg')
            # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            # plt.rcParams['axes.unicode_minus'] = False
            # plt.plot(df.iloc[:, 0], df.iloc[:, 1])
            # plt.xlabel('管长')
            # plt.ylabel('振动位移')
            # plt.title('振动位移随管长变化')
            # plt.show()
            show_moulde3_image(self)
        except Exception as e:

            print("===== process error ======")
            print("模块三计算失败")
            QMessageBox.information(self, "错误", str(e))


# def matlab_function():
#     eng = matlab.engine.start_matlab()
#     eng.cd('matlab2')
#     eng.mainfunc(nargout=0)
#     print("Compute complete")
#     eng.quit()
#     return True


def setParameters(self):
    global saved_data
    saved_data = result_form.moudle3_inform_2
    self.label_75.setText(str(saved_data))
    if result_form.moudle3_inform is not None:
        self.lineEdit_a1.setText(result_form.moudle3_inform[0])
        self.lineEdit_a2.setText(result_form.moudle3_inform[1])
        self.lineEdit_a3.setText(result_form.moudle3_inform[2])
        self.lineEdit_a4.setText(result_form.moudle3_inform[3])
        self.lineEdit_a5.setText(result_form.moudle3_inform[4])
        self.lineEdit_a6.setText(result_form.moudle3_inform[5])
        self.lineEdit_a7.setText(result_form.moudle3_inform[6])


def getParameters(self):
    data = [self.lineEdit_a1.text(), self.lineEdit_a2.text(), self.lineEdit_a3.text(), self.lineEdit_a4.text(),
            self.lineEdit_a5.text(), self.lineEdit_a6.text(), self.lineEdit_a7.text()]
    return data

def show_moulde3_image(self):
    if result_form.moudle3_flag:
        df = result_form.moudle3_result
        # 使用前两列数据生成图像
        plt.switch_backend('Qt5Agg')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        F1 = MyFigure(width=5, height=4, dpi=100)
        F1.axes1 = F1.fig.add_subplot(111)
        F1.axes1.plot(df.iloc[:, 0], df.iloc[:, 1], 'r')
        F1.axes1.set_xlabel('管长 (m)', fontsize=11)
        F1.axes1.set_ylabel('振动位移 (m)', fontsize=11)
        F1.axes1.set_title('振动位移随管长变化')
        width, height = self.graphicsView_5.width(), self.graphicsView_5.height()
        F1.resize(width, height)
        self.scene = QGraphicsScene()  # 创建一个场景
        self.scene.addWidget(F1)  # 将图形元素添加到场景中
        self.graphicsView_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView_5.setScene(self.scene)  # 将创建添加到图形视图显示窗口
    else:
        QMessageBox.information(self, "错误", "未有数据输入，请先输入数据并计算")