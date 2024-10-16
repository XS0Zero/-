import math
import re

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene
from matplotlib import pyplot as plt

import matlab_project.main
from ctrl.result_slot import MyFigure
from data import result_form
from matlab_project import MAXQd, Mz
from matlab_project.BWRSV1 import BWRSV1_func
from matlab_project.BWRSV2 import BWRSV2_func
from matlab_project.JL3 import JL_func

result = None
Qg, Ql, P1, Pflq, T1, D, n, LL, r1 = 0, 0, 0, 0, 0, 0, 0, 0, 0
r2 = None


def on_compute_button_clicked(self):
    try:
        result_form.Px1 = []
        result_form.Tx1 = []
        result_form.G1 = result_form.G2 = result_form.G3 = 0
        global result, Qg, Ql, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3, r1, r2
        print("Compute button clicked")
        Qg = self.QgEdit.toPlainText()
        Ql = self.QlEdit.toPlainText()

        P1 = self.P1Edit.toPlainText()
        Pflq = self.PflqEdit.toPlainText()
        T1 = self.T1Edit.toPlainText()
        D = self.DEdit.toPlainText()
        n = self.nEdit.toPlainText()
        L = self.LEdit.toPlainText()

        LL = self.LLEdit.toPlainText()
        LL1 = self.LL1Edit.toPlainText()
        LL2 = self.LL2Edit.toPlainText()
        LL3 = self.LL3Edit.toPlainText()

        if any(isinstance(x, str) and x == '' for x in [Qg, Ql, P1, Pflq, T1, D, n, LL]):
            Qg, Ql, P1, Pflq, T1, D, n, L, LL, LL1, LL2, LL3 = [0 if isinstance(x, str) and x == '' else x for x in
                                                                [Qg, Ql, P1, Pflq, T1, D, n, L, LL, LL1, LL2, LL3]]

        MAXQd.L = float(L)
        result_form.L = float(L)
        result_form.Pflq = Pflq

        if self.tabWidget.currentIndex() == 0:
            r1 = self.rEdit.toPlainText()
            if r1 == '':
                r1 = 0
        if self.tabWidget.currentIndex() == 1:
            r2 = getR(self)

        if LL != 0:
            try:
                n1 = self.nEdit_2.text()
                if n1 == '':
                    n1 = 0
                else:
                    n1 = int(n1)  # 一级节流前弯头个数
                result_form.n1 = n1
                LL = float(LL)
                result_form.LL = LL
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
        else:
            n1 = 0
        print('一级节流前弯头个数', n1)
        # LL_list = re.split(',|，', LL)
        # LL = np.zeros((1, n1 + 1))
        # for item in LL_list:
        #     # print(item)
        #     LL[0, LL_list.index(item)] = item
        # print(LL)

        if LL1 != 0:
            try:
                n2 = self.nEdit_3.text()
                if n2 == '':
                    n2 = 0
                else:
                    n2 = int(n2)
                result_form.n2 = n2
                LL1 = float(LL1)
                result_form.LL1 = LL1
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
        else:
            n2 = 0
        print('二级节流前弯头个数', n2)
        # LL1_list = re.split(',|，', LL1)
        # LL1 = np.zeros((1, n2 + 1))
        # for item in LL1_list:
        #     # print(item)
        #     LL1[0, LL1_list.index(item)] = item
        # print(LL1)

        if LL2 != 0:
            try:
                n3 = self.nEdit_4.text()
                if n3 == '':
                    n3 = 0
                else:
                    n3 = int(n3)
                result_form.n3 = n3
                LL2 = float(LL2)
                result_form.LL2 = LL2
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
        else:
            n3 = 0
        print('三级节流前弯头个数', n3)
        # LL2_list = re.split(',|，', LL2)
        # LL2 = np.zeros((1, n3 + 1))
        # for item in LL2_list:
        #     # print(item)
        #     LL2[0, LL2_list.index(item)] = item
        # # print(LL2)

        if LL3 != 0:
            try:
                n4 = self.nEdit_4.text()
                if n4 == '':
                    n4 = 0
                else:
                    n4 = int(n4)
                result_form.n4 = n4
                LL3 = float(LL3)
                result_form.LL3 = LL3
            except ValueError:
                QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
        else:
            n4 = 0
        print('三级节流到分离器前弯头个数', n4)
        # LL3_list = re.split(',|，', LL3)
        # LL3 = np.zeros((1, n4 + 1))
        # for item in LL3_list:
        #     # print(item)
        #     LL3[0, LL3_list.index(item)] = item
        # print(LL3)

        # print(Qg, Ql, r, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3)

        if self.tabWidget.currentIndex() == 1:
            result = matlab_project.main.compute(float(Qg), float(Ql), r2, float(P1), float(Pflq), float(T1),
                                                 float(D),
                                                 int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))
        if self.tabWidget.currentIndex() == 0:
            print("相对密度形式输入")
            result = matlab_project.main.compute(float(Qg), float(Ql), float(r1), float(P1), float(Pflq), float(T1),
                                                 float(D),
                                                 int(n), LL, LL1, LL2, LL3, int(n1), int(n2), int(n3), int(n4))
        result = list(result)
        print(result)
        if result is None:
            QMessageBox.information(self, "错误", "参数输入有误")
            return
        result = [
            str(round(result[0] if result[0] is not None else 0.0, 2)),
            str(round(result[1] if result[1] is not None else 0.0, 2)),
            str(round(result[2] if result[2] is not None else 0.0, 2)),
            str(round(result[3] if result[3] is not None else 0.0, 2)),
            str(round(result[4] if result[4] is not None else 0.0, 2)),
            str(round(result[5] if result[5] is not None else 0.0, 2)),
            str(round(result[6] if result[6] is not None else 0.0, 2)),
            str(round(result[7] if result[7] is not None else 0.0, 2)),
            str(round(result[8] if result[8] is not None else 0.0, 2)),
            str(result[9]),
            str(result[10]),
            str(result[11]),
            str(round(np.sum(result[12]) if result[12] is not None else 0.0, 2)),
            str(round(np.sum(result[13]) if result[13] is not None else 0.0, 2)),
            str(round(np.sum(result[14]) if result[14] is not None else 0.0, 2)),
            str(round(np.sum(result[15]) if result[15] is not None else 0.0, 2)),
            str(result[16])
        ]

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
        # self.P2.setText(result[9])
        # self.P22.setText(result[10])
        self.P222.setText(result[11])
        self.Pctiz1.setText(result[12])
        self.Pctiz2.setText(result[13])
        self.Pctiz3.setText(result[14])
        self.Pctiz4.setText(result[15])
        self.Qd.setText(result[16])

        print('水合物抑制剂')
        print(result_form.G1, result_form.G2, result_form.G3)
        str1 = ''
        if result_form.G1 != 0:
            str1 += f"一级水合物抑制剂：{round(result_form.G1, 2)}kg/d"
        if result_form.G2 != 0:
            str1 += f"\n二级水合物抑制剂：{round(result_form.G2, 2)}kg/d"
        if result_form.G3 != 0:
            str1 += f"\n三级水合物抑制剂：{round(result_form.G3, 2)}kg/d"
        self.label_56.setText(str1)
        show_moulde1_image(self)
        QMessageBox.information(self, "提示", "计算完成")
    except Exception as e:
        QMessageBox.warning(self, "错误", f"错误：{e}")


# 甲烷、乙烷、丙烷、异丁烷、正丁烷、异戊烷、正戊烷、氮气、二氧化碳、硫化氢
# 当选择为组分时获取气体组分数据
def getR(self):
    global r
    r = []
    for i in range(1, 11):
        try:
            r.append(float(getattr(self, f'lineEdit_r{i}').text()))
        except ValueError:
            print("请输入正确的气体组分数据")
            return False
    return r


# 存储和读取参数
def getparameter(self):
    Qg = self.QgEdit.toPlainText()
    Ql = self.QlEdit.toPlainText()

    P1 = self.P1Edit.toPlainText()
    Pflq = self.PflqEdit.toPlainText()
    T1 = self.T1Edit.toPlainText()
    D = self.DEdit.toPlainText()
    n = self.nEdit.toPlainText()

    n1 = self.nEdit_2.text()
    n2 = self.nEdit_3.text()
    n3 = self.nEdit_4.text()
    n4 = self.nEdit_5.text()
    L = self.LEdit.toPlainText()

    r1 = self.rEdit.toPlainText()
    r2 = getR(self)

    LL = self.LLEdit.toPlainText()
    LL1 = self.LL1Edit.toPlainText()
    LL2 = self.LL2Edit.toPlainText()
    LL3 = self.LL3Edit.toPlainText()

    if any(isinstance(x, str) and x == '' for x in
           [Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2]):
        Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2 = [
            '0' if isinstance(x, str) and x == '' else x for x in
            [Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2]]
    return Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2


def setparameter(self):
    self.QgEdit.setText(str(result_form.Qg))
    self.QlEdit.setText(str(result_form.Ql))
    self.P1Edit.setText(str(result_form.P1))
    self.PflqEdit.setText(str(result_form.Pflq))
    self.T1Edit.setText(str(result_form.T1))
    self.DEdit.setText(str(result_form.D))
    self.nEdit.setText(str(result_form.n))
    self.nEdit_2.setText(str(result_form.n1))
    self.nEdit_3.setText(str(result_form.n2))
    self.nEdit_4.setText(str(result_form.n3))
    self.nEdit_5.setText(str(result_form.n4))
    self.LEdit.setText(str(result_form.L))
    self.LLEdit.setText(str(result_form.LL))
    self.LL1Edit.setText(str(result_form.LL1))
    self.LL2Edit.setText(str(result_form.LL2))
    self.LL3Edit.setText(str(result_form.LL3))
    for i in range(1, 11):
        try:
            getattr(self, f'lineEdit_r{i}').setText(str(result_form.r2[i - 1]))
        except (ValueError, TypeError, IndexError):
            print("请输入正确的气体组分数据")
    if result_form.r1 is not None:
        self.rEdit.setText(str(result_form.r1))
    str1 = ''
    if result_form.G1 != 0:
        str1 += f"一级水合物抑制剂：{round(result_form.G1, 2)}kg/d"
    if result_form.G2 != 0:
        str1 += f"\n二级水合物抑制剂：{round(result_form.G2, 2)}kg/d"
    if result_form.G3 != 0:
        str1 += f"\n三级水合物抑制剂：{round(result_form.G3, 2)}kg/d"
    self.label_56.setText(str1)


# 存储和读取结果
def getresult():
    return result


def setresult(self):
    result = result_form.jieliu_result
    if result is not None:
        self.d_label.setText(result[0])
        self.dd_label.setText(result[1])
        self.ddd_label.setText(result[2])
        self.T2_label.setText(result[3])
        self.T22_label.setText(result[4])
        self.T222_label.setText(result[5])
        self.P1jl.setText(result[6])
        self.P2jl.setText(result[7])
        self.P3jl.setText(result[8])
        # self.P2.setText(result[9])
        # self.P22.setText(result[10])
        self.P222.setText(result[11])
        self.Pctiz1.setText(result[12])
        self.Pctiz2.setText(result[13])
        self.Pctiz3.setText(result[14])
        self.Pctiz4.setText(result[15])
        self.Qd.setText(result[16])


def compute_pctiz(self):
    global Qg, Ql, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3, r1, r2
    print("compute_pctiz")
    Qg = self.QgEdit.toPlainText()
    Ql = self.QlEdit.toPlainText()

    P1 = self.P1Edit.toPlainText()
    Pflq = self.PflqEdit.toPlainText()
    T1 = self.T1Edit.toPlainText()
    D = self.DEdit.toPlainText()
    n = self.nEdit.toPlainText()
    L = self.LEdit.toPlainText()

    LL = self.LLEdit.toPlainText()
    LL1 = self.LL1Edit.toPlainText()
    LL2 = self.LL2Edit.toPlainText()
    LL3 = self.LL3Edit.toPlainText()

    if any(isinstance(x, str) and x == '' for x in [Qg, Ql, P1, Pflq, T1, D, n, LL]):
        Qg, Ql, P1, Pflq, T1, D, n, L, LL, LL1, LL2, LL3 = [0 if isinstance(x, str) and x == '' else x for x in
                                                            [Qg, Ql, P1, Pflq, T1, D, n, L, LL, LL1, LL2, LL3]]
    try:
        Qg = float(Qg)
        Ql = float(Ql)
        P1 = float(P1)
        Pflq = float(Pflq)
        T1 = float(T1)
        D = float(D)
        n = float(n)
        L = float(L)
    except ValueError:
        QMessageBox.warning(self, '错误', '请正确填入所需数据')

    MAXQd.L = float(L)
    result_form.L = float(L)

    if self.tabWidget.currentIndex() == 0:
        r1 = self.rEdit.toPlainText()
        if r1 == '':
            r1 = 0
    if self.tabWidget.currentIndex() == 1:
        r2 = getR(self)

    if LL != 0:
        try:
            n1 = self.nEdit_2.text()
            if n1 == '':
                n1 = 0
            else:
                n1 = int(n1)  # 一级节流前弯头个数
            result_form.n1 = n1
            LL = float(LL)
            result_form.LL = LL
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
    else:
        n1 = 0
    print('一级节流前弯头个数', n1)

    if LL1 != 0:
        try:
            n2 = self.nEdit_3.text()
            if n2 == '':
                n2 = 0
            else:
                n2 = int(n2)
            result_form.n2 = n2
            LL1 = float(LL1)
            result_form.LL1 = LL1
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
    else:
        n2 = 0
    print('二级节流前弯头个数', n2)

    if LL2 != 0:
        try:
            n3 = self.nEdit_4.text()
            if n3 == '':
                n3 = 0
            else:
                n3 = int(n3)
            result_form.n3 = n3
            LL2 = float(LL2)
            result_form.LL2 = LL2
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
    else:
        n3 = 0
    print('三级节流前弯头个数', n3)

    if LL3 != 0:
        try:
            n4 = self.nEdit_4.text()
            if n4 == '':
                n4 = 0
            else:
                n4 = int(n4)
            result_form.n4 = n4
            LL3 = float(LL3)
            result_form.LL3 = LL3
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入正确的弯头个数')
    else:
        n4 = 0
    print('三级节流到分离器前弯头个数', n4)
    T0 = float(T1) + 273.15
    if self.tabWidget.currentIndex() == 1:
        r = r2
        try:
            len(r)
            r = BWRSV2_func(P1, T0, r)
            r = float(r[0])
            r = round(r, 2)
        except TypeError:
            print("相对密度形式输入")
    if self.tabWidget.currentIndex() == 0:
        print("相对密度形式输入")
        r = float(r1)


    Lep = 30 * D * 1
    try:
        BWRSV1 = BWRSV1_func(P1, T0)
        Z0 = BWRSV1[0]
        Bg = 3.447e-4 * Z0 * T0 / P1
        V0 = 4 * Qg * Bg / 86400 / math.pi / D ** 2
        den0 = BWRSV1[2]
        LL = LL + n1 * Lep
        Pctiz1 = round(Mz.Pctiz_func(V0, LL, D, den0), 2)
        result_form.jieliu_result[12] = str(Pctiz1)
        self.Pctiz1.setText(str(Pctiz1))
    except Exception as e:
        QMessageBox.warning(self, "错误", str(e))
    R = 8.314  # 气体常数
    k = 1.2917  # 比热容比
    Tci = 190.69  # 临界温度，K
    Pci = 4.64  # 临界压力,Pa
    try:
        if r >= 0.7:
            Pc = (4881 - 386.11 * r) / 1000  # 压力,MPa
            Tc = 92 + 176.67 * r  # 温度,℃
        else:
            Pc = (4778 - 248.21 * r) / 1000  # 压力,MPa
            Tc = 92 + 176.67 * r  # 温度,℃
        P2, T2, d, Qg1, Z1 = JL_func(P1, T1, Qg, r, k, R, Pc, Tc, Pci, Tci)
        Twash = T2 + 273.15
        BWRSV1 = BWRSV1_func(P2, Twash)
        Z2 = BWRSV1[0]  # 一级节流后的压缩因子

        r2 = BWRSV1[1][0][0]
        Vc = (Qg1 * Twash * 0.404 * Z2) / (8.64 * 293 * P2 * math.pi * (d * 0.1) ** 2)
        LL1 = LL1 + n2 * Lep
        Pctiz2 = round(Mz.Pctiz_func(Vc, LL1, D, r2), 2)
        result_form.jieliu_result[13] = str(Pctiz2)
        self.Pctiz2.setText(str(Pctiz2))
    except Exception as e:
        Pctiz2 = 0
        self.Pctiz2.setText(str(Pctiz2))
        # QMessageBox.warning(self, "错误", str(e))
    while True:
        try:
            if P2 > Pflq:
                P11 = P2  # 一级节流后压力（减掉摩阻）
            else:
                Pctiz3 = 0
                self.Pctiz3.setText(str(Pctiz3))
                break
            T11 = T2  # 一级节流后温度
            P22, T22, dd, Qg11, __ = JL_func(P11, T11, Qg, r, k, R, Pc, Tc, Pci, Tci)
            Twash2 = T22 + 273.15  # 二级节流后温度，K
            r22 = BWRSV1_func(P22, Twash2)[1][0][0]  # 二级节流后的压缩因子
            Z22 = BWRSV1_func(P22, Twash2)[0]
            Vcc = (Qg11 * Twash2 * 0.404 * Z22) / (8.64 * 293 * P22 * math.pi * (dd * 0.1) ** 2)  # 一级节流嘴流速 m/s
            LL2 = LL2 + n3 * Lep
            Pctiz3 = round(Mz.Pctiz_func(Vcc, LL2, D, r22), 2)
            result_form.jieliu_result[14] = str(Pctiz3)
            self.Pctiz3.setText(str(Pctiz3))
            break
        except Exception as e:
            Pctiz3 = 0
            self.Pctiz3.setText(str(Pctiz3))
            # QMessageBox.warning(self, "错误", str(e))
            break
    while True:
        try:
            if P22 > Pflq and P22 > 9:
                P111 = P22  # 二级节流后压力（减掉摩阻后）
            else:
                Pctiz4 = 0
                self.Pctiz4.setText(str(Pctiz4))
                break
            T111 = T22  # 二级节流后温度
            P222, T222, ddd, Qg111, __ = JL_func(P111, T111, Qg, r, k, R, Pc, Tc, Pci, Tci)
            Twash3 = T222 + 273.15  # 二级节流后温度，K
            r222 = BWRSV1_func(P222, Twash3)[1][0][0]  # 二级节流后的压缩因子
            Z222 = BWRSV1_func(P222, Twash3)[0]
            Vccc = (Qg111 * Twash3 * 0.404 * Z222) / (8.64 * 293 * P222 * 3.1415926 * (ddd * 0.1) ** 2)  # 一级节流嘴流速 m/s
            LL3 = LL3 + n4 * Lep
            Pctiz4 = round(Mz.Pctiz_func(Vccc, LL3, D, r222), 2)
            result_form.jieliu_result[15] = str(Pctiz4)
            self.Pctiz4.setText(str(Pctiz4))
            break
        except Exception as e:
            Pctiz4 = 0
            self.Pctiz4.setText(str(Pctiz4))
            # QMessageBox.warning(self, "错误", str(e))
            break


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

            width, height = self.graphicsView_3.width(), self.graphicsView_3.height()
            F1.resize(width, height)
            self.scene = QGraphicsScene()  # 创建一个场景
            self.scene.addWidget(F1)  # 将图形元素添加到场景中
            self.graphicsView_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.graphicsView_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.graphicsView_3.setScene(self.scene)  # 将创建添加到图形视图显示窗口
        else:
            QMessageBox.information(self, "错误", "未有数据输入，请先输入数据并计算")
    except Exception as e:
        QMessageBox.information(self, "错误", str(e))
