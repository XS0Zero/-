import os

import matlab.engine
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem
from pandas.errors import EmptyDataError

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
            flag = 1
            break
    index = 0
    for i in saved_data:
        if not check_input(i):
            print("存在错误输入参数")
            flag = 1
            break
        inputdata.iloc[7, index] = float(i)
        index += 1

    if flag == 0:
        for i in range(7):
            inputdata.iloc[i, 0] = float(data[i])

        inputdata.to_csv(r'matlab2/输入数据.csv', index=False, header=False)
        print(inputdata)
        print("开始调用matlab函数")
        matlab_function()
        print("模块三计算完成")

        df = pd.read_csv('matlab2/振动位移随管长变化.csv')
        # 获取行数和列数
        rows, cols = df.shape

        # 设置表格的行数和列数
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)

        # 读取数据并显示在表格中
        for i in range(rows):
            for j in range(cols):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


def matlab_function():
    eng = matlab.engine.start_matlab()
    eng.cd('matlab2')
    eng.mainfunc(nargout=0)
    print("Compute complete")
    eng.quit()
    return True


if __name__ == '__main__':
    matlab_function()
