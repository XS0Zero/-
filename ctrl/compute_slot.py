import os

import matlab.engine
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from matplotlib import pyplot as plt
from pandas.errors import EmptyDataError

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
        inputdata = pd.read_csv(r'matlab2/输入数据.csv', sep=',', header=None)
    except EmptyDataError:
        inputdata = pd.DataFrame(index=range(8), columns=range(6))
    print(inputdata)
    print(inputdata.iloc[:, 0])

    def check_input(input_value):
        try:
            float(input_value)
            return True
        except ValueError:
            return False

    data = [0] * 7
    flag = 0
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
        inputdata.iloc[7, index] = float(i)
        index += 1

    result_form.moudle3_inform = data
    result_form.moudle3_inform_2 = saved_data

    if flag == 0:
        for i in range(7):
            inputdata.iloc[i, 0] = float(data[i])

        inputdata.to_csv(r'matlab2/输入数据.csv', index=False, header=False)
        print(inputdata)
        print("开始调用matlab函数")
        # QMessageBox.information(self, "提示", "计算中，请稍后...")
        matlab_function()
        print("模块三计算完成")
        QMessageBox.information(self, "提示", "模块三计算完成")
        result_form.moudle3_flag = True

        df = pd.read_csv('matlab2/振动位移随管长变化.csv')

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
        plt.switch_backend('Qt5Agg')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False
        plt.plot(df.iloc[:, 0], df.iloc[:, 1])
        plt.xlabel('管长')
        plt.ylabel('振动位移')
        plt.title('振动位移随管长变化')
        plt.show()


def matlab_function():
    eng = matlab.engine.start_matlab()
    eng.cd('matlab2')
    eng.mainfunc(nargout=0)
    print("Compute complete")
    eng.quit()
    return True


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

if __name__ == '__main__':
    matlab_function()
