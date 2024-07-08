import re

import numpy as np

import matlab_project.main

result = None
jieliu_parameter = [0]*12

def on_compute_button_clicked(self):
    global result
    print("Compute button clicked")
    Qg = self.QgEdit.toPlainText()
    Ql = self.QlEdit.toPlainText()
    r = self.rEdit.toPlainText()
    P1 = self.P1Edit.toPlainText()
    Pflq = self.PflqEdit.toPlainText()
    T1 = self.T1Edit.toPlainText()
    D = self.DEdit.toPlainText()
    n = self.nEdit.toPlainText()

    LL = self.LLEdit.toPlainText()

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

    global jieliu_parameter

    jieliu_parameter = [Qg, Ql, r, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3]

    print(Qg, Ql, r, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3)

    result = matlab_project.main.compute(float(Qg), float(Ql), float(r), float(P1), float(Pflq), float(T1), float(D),
                                         int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))
    print(result)
    # return d, dd, ddd, T2, T22, T222, P1j1, P1j2, P1j3, P2_bool, P22_bool, P222_bool, Pctiz1, Pctiz2, Pctiz3, Pctiz4, Qd
    self.d_label.setText(str(round(result[0], 2)))  # round(result[0],2)
    self.dd_label.setText(str(round(result[1], 2)))
    self.ddd_label.setText(str(round(result[2], 2)))
    self.T2_label.setText(str(round(result[3], 2)))
    self.T22_label.setText(str(round(result[4], 2)))
    self.T222_label.setText(str(round(result[5], 2)))
    self.P1jl.setText(str(round(result[6], 2)))
    self.P2jl.setText(str(round(result[7], 2)))
    self.P3jl.setText(str(round(result[8], 2)))
    self.P2.setText(str(result[9]))
    self.P22.setText(str(result[10]))
    self.P222.setText(str(result[11]))
    self.Pctiz1.setText(str(np.round(np.sum(result[12]), 2)))
    self.Pctiz2.setText(str(np.round(np.sum(result[13]), 2)))
    self.Pctiz3.setText(str(np.round(np.sum(result[14]), 2)))
    self.Pctiz4.setText(str(np.round(np.sum(result[15]), 2)))
    self.Qd.setText(str(result[16]))


# 存储和读取参数
def getparameter():
    return jieliu_parameter


def setparameter(par):
    global jieliu_parameter
    jieliu_parameter = par


# 存储和读取结果
def getresult():
    return result


def setresult(res):
    global result
    result = res
