import re

import numpy as np

import matlab_project.main
from data import result_form

result = None


def on_compute_button_clicked(self):
    global result
    print("Compute button clicked")
    Qg = self.QgEdit.toPlainText()
    Ql = self.QlEdit.toPlainText()

    P1 = self.P1Edit.toPlainText()
    Pflq = self.PflqEdit.toPlainText()
    T1 = self.T1Edit.toPlainText()
    D = self.DEdit.toPlainText()
    n = self.nEdit.toPlainText()

    LL = self.LLEdit.toPlainText()

    result_form.jieliu_inform = [Qg, Ql, P1, Pflq, T1, D, n, LL]

    if self.tabWidget.currentIndex() == 0:
        r = self.rEdit.toPlainText()
    if self.tabWidget.currentIndex() == 1:
        r = getR(self)

    n1 = LL.count(',') + LL.count('，')  # 一级节流前弯头个数
    print('一级节流前弯头个数', n1)
    LL_list = re.split(',|，', LL)
    LL = np.zeros((1, n1 + 1))
    for item in LL_list:
        print(item)
        LL[0, LL_list.index(item)] = item
    print(LL)

    LL1 = self.LL1Edit.toPlainText()

    n2 = LL1.count(',') + LL1.count('，')  # 二级节流前弯头个数
    print('二级节流前弯头个数', n2)
    LL1_list = re.split(',|，', LL1)
    LL1 = np.zeros((1, n2 + 1))
    for item in LL1_list:
        print(item)
        LL1[0, LL1_list.index(item)] = item
    print(LL1)

    LL2 = self.LL2Edit.toPlainText()

    n3 = LL2.count(',') + LL2.count('，')  # 三级节流前弯头个数
    print('三级节流前弯头个数', n3)
    LL2_list = re.split(',|，', LL2)
    LL2 = np.zeros((1, n3 + 1))
    for item in LL2_list:
        print(item)
        LL2[0, LL2_list.index(item)] = item
    print(LL2)

    LL3 = self.LL3Edit.toPlainText()

    n4 = LL3.count(',') + LL3.count('，')  # 三级节流到分离器前
    print('三级节流到分离器前弯头个数', n4)
    LL3_list = re.split(',|，', LL3)
    LL3 = np.zeros((1, n4 + 1))
    for item in LL3_list:
        print(item)
        LL3[0, LL3_list.index(item)] = item
    print(LL3)



    print(Qg, Ql, r, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3)

    try:
        len(r)
        result = matlab_project.main.compute(float(Qg), float(Ql), r, float(P1), float(Pflq), float(T1),
                                             float(D),
                                             int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))
    except TypeError:
        print("相对密度形式输入")
        result = matlab_project.main.compute(float(Qg), float(Ql), float(r), float(P1), float(Pflq), float(T1),
                                             float(D),
                                             int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))

    print(result)
    result = [str(round(result[0], 2)), str(round(result[1], 2)), str(round(result[2], 2)), str(round(result[3], 2)), str(round(result[4], 2)),
                str(round(result[5], 2)), str(round(result[6], 2)), str(round(result[7], 2)), str(round(result[8], 2)), str(result[9]), str(result[10]), str(result[11]),
                str(np.round(np.sum(result[12]), 2)), str(np.round(np.sum(result[13]), 2)), str(np.round(np.sum(result[14]), 2)), str(np.round(np.sum(result[15]), 2)), str(result[16])]
    result_form.jieliu_result = result
    # return d, dd, ddd, T2, T22, T222, P1j1, P1j2, P1j3, P2_bool, P22_bool, P222_bool, Pctiz1, Pctiz2, Pctiz3, Pctiz4, Qd
    self.d_label.setText(result[0])  # round(result[0],2)
    self.dd_label.setText(result[1])
    self.ddd_label.setText(result[2])
    self.T2_label.setText(result[3])
    self.T22_label.setText(result[4])
    self.T222_label.setText(result[5])
    self.P1jl.setText(result[6])
    self.P2jl.setText(result[7])
    self.P3jl.setText(result[8])
    self.P2.setText(result[9])
    self.P22.setText(result[10])
    self.P222.setText(result[11])
    self.Pctiz1.setText(result[12])
    self.Pctiz2.setText(result[13])
    self.Pctiz3.setText(result[14])
    self.Pctiz4.setText(result[15])
    self.Qd.setText(result[16])


# 甲烷、乙烷、丙烷、异丁烷、正丁烷、异戊烷、正戊烷、氮气、二氧化碳、硫化氢
# 当选择为组分时获取气体组分数据
def getR(self):
    r = []
    for i in range(1, 11):
        try:
            r.append(float(getattr(self, f'lineEdit_r{i}').text()))
        except ValueError:
            print("请输入正确的气体组分数据")
            return False
    return r


# 存储和读取参数
def getparameter():
    return result_form.jieliu_inform


def setparameter(self):
    self.QgEdit.setText(str(result_form.jieliu_inform[0]))
    self.QlEdit.setText(str(result_form.jieliu_inform[1]))
    self.P1Edit.setText(str(result_form.jieliu_inform[2]))
    self.PflqEdit.setText(str(result_form.jieliu_inform[3]))
    self.T1Edit.setText(str(result_form.jieliu_inform[4]))
    self.DEdit.setText(str(result_form.jieliu_inform[5]))
    self.nEdit.setText(str(result_form.jieliu_inform[6]))
    self.LLEdit.setText(str(result_form.jieliu_inform[7]))


# 存储和读取结果
def getresult():
    return result


def setresult(self):
    result = result_form.jieliu_result
    # return d, dd, ddd, T2, T22, T222, P1j1, P1j2, P1j3, P2_bool, P22_bool, P222_bool, Pctiz1, Pctiz2, Pctiz3, Pctiz4, Qd
    self.d_label.setText(result[0])  # round(result[0],2)
    self.dd_label.setText(result[1])
    self.ddd_label.setText(result[2])
    self.T2_label.setText(result[3])
    self.T22_label.setText(result[4])
    self.T222_label.setText(result[5])
    self.P1jl.setText(result[6])
    self.P2jl.setText(result[7])
    self.P3jl.setText(result[8])
    self.P2.setText(result[9])
    self.P22.setText(result[10])
    self.P222.setText(result[11])
    self.Pctiz1.setText(result[12])
    self.Pctiz2.setText(result[13])
    self.Pctiz3.setText(result[14])
    self.Pctiz4.setText(result[15])
    self.Qd.setText(result[16])
