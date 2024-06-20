import re

import numpy as np

import matlab_project.main


def on_compute_button_clicked(self):
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

    print(Qg, Ql, r, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3)

    result = matlab_project.main.compute(float(Qg), float(Ql), float(r), float(P1), float(Pflq), float(T1), float(D),
                                         int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))
    print(result)
    # return d, dd, ddd, T2, T22, T222, P1j1, P1j2, P1j3, P2_bool, P22_bool, P222_bool, Pctiz1, Pctiz2, Pctiz3, Pctiz4, Qd
    self.d_label.setText(str(result[0]))  # round(result[0],2)
    self.dd_label.setText(str(result[1]))
    self.ddd_label.setText(str(result[2]))
    self.T2_label.setText(str(result[3]))
    self.T22_label.setText(str(result[4]))
    self.T222_label.setText(str(result[5]))
    self.P1jl.setText(str(result[6]))
    self.P2jl.setText(str(result[7]))
    self.P3jl.setText(str(result[8]))
    self.P2.setText(str(result[9]))
    self.P22.setText(str(result[10]))
    self.P222.setText(str(result[11]))
    self.Pctiz1.setText(str(result[12]))
    self.Pctiz2.setText(str(result[13]))
    self.Pctiz3.setText(str(result[14]))
    self.Pctiz4.setText(str(result[15]))
    self.Qd.setText(str(result[16]))
