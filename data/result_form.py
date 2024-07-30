import ast
import io
import os

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

from ctrl import Jieliu_slot, compute_slot
from ctrl.Jieliu_slot import getparameter
from ctrl.menu_slot import change_page

Project_inform = None
image_base64 = None

jieliu_result = None
moudle3_inform = None
moudle3_inform_2 = None
moudle3_result = None
# 模块3运行后设为true，避免遗留数据影响
moudle3_flag = False
Vc = None
Vcc = None
Vccc = None
Ve = None
Vee = None
Veee = None

Qg = None
Ql = None
P1 = None
Pflq = None
T1 = None
D = None
n = None
n1 = 0
n2 = 0
n3 = 0
n4 = 0
L = 0
# LL_n1 = 0
# LL1_n2 = 0
# LL2_n3 = 0
# LL3_n4 = 0
LL = None
LL1 = None
LL2 = None
LL3 = None
r1 = None
r2 = None
G1 = None
G2 = None
G3 = None
P2 = None
P22 = None
P222 = None
T2 = None
T22 = None
T222 = None
Px1 = []
Tx1 = []


# 保存工程
def save_project(self, path):
    global Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2, moudle3_result, Tx1
    Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2 = Jieliu_slot.getparameter(self)
    try:
        moudle3_result.to_string(index=False, header=False)
    except AttributeError:
        moudle3_result = pd.DataFrame()
    try:
        Px1_1 = str(Px1[0].tolist())
        Px1_2 = str(Px1[1].tolist())
        Px1_3 = str(Px1[2].tolist())
        Tx1[0] = Tx1[0][1:]
        Tx1[1] = Tx1[1][1:]
        Tx1[2] = Tx1[2][1:]
        Tx1_1 = str(Tx1[0].tolist())
        Tx1_2 = str(Tx1[1].tolist())
        Tx1_3 = str(Tx1[2].tolist())
    except IndexError:
        Px1_1 = Px1_2 = Px1_3 = Tx1_1 = Tx1_2 = Tx1_3 = ''
    except AttributeError:
        Px1_1 = str(Px1[0])
        Px1_2 = str(Px1[1])
        Px1_3 = str(Px1[2])
        Tx1_1 = str(Tx1[0])
        Tx1_2 = str(Tx1[1])
        Tx1_3 = str(Tx1[2])
    try:
        moudle3_inform = compute_slot.getParameters(self)
    except Exception as e:
        pass
    # np.set_printoptions(threshold=10000)
    df = pd.DataFrame({
        'Project_inform': [Project_inform],
        'image_base64': [image_base64],
        'Qg': [Qg],
        'Ql': [Ql],
        'P1': [P1],
        'Pflq': [Pflq],
        'T1': [T1],
        'D': [D],
        'n': [n],
        'n1': [n1],
        'n2': [n2],
        'n3': [n3],
        'n4': [n4],
        'L': [L],
        'LL': [LL],
        'LL1': [LL1],
        'LL2': [LL2],
        'LL3': [LL3],
        'r1': [r1],
        'r2': [r2],
        'jieliu_result': [jieliu_result],
        'moudle3_inform': [moudle3_inform],
        'moudle3_inform_2': [moudle3_inform_2],
        'moudle3_result': [moudle3_result.to_string(index=False, header=False)],
        'moudle3_flag': [moudle3_flag],
        'Vc': [Vc],
        'Vcc': [Vcc],
        'Vccc': [Vccc],
        'Ve': [Ve],
        'Vee': [Vee],
        'Veee': [Veee],
        'G1': [G1],
        'G2': [G2],
        'G3': [G3],
        'P2': [P2],
        'P22': [P22],
        'P222': [P222],
        'T2': [T2],
        'T22': [T22],
        'T222': [T222],
        'Px1_1': [Px1_1],
        'Tx1_1': [Tx1_1],
        'Px1_2': [Px1_2],
        'Tx1_2': [Tx1_2],
        'Px1_3': [Px1_3],
        'Tx1_3': [Tx1_3],
    })
    print(df)
    # 检查文件是否存在
    if os.path.exists(path):
        try:
            # 如果文件存在，则覆盖文件
            file = open(path, 'w')
            df.to_csv(file, index=False, mode='w')
            QMessageBox.information(self, "提示", "保存成功")
        except PermissionError:
            print("文件被占用，请关闭文件后重试")
            QMessageBox.information(self, "提示", "文件被占用，请关闭文件后重试")
    else:
        # 如果文件不存在，则创建新文件
        df.to_csv(path, index=False)
        QMessageBox.information(self, "提示", "保存成功")


def open_project(self, path):
    global Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2, moudle3_result, G1, G2, G3
    global P2, P22, P222, T2, T22, T222, Px1, Tx1
    Px1 = []
    Tx1 = []
    try:
        df = pd.read_csv(path, encoding='gbk')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='utf-8')
    print(df)

    global Project_inform, image_base64, jieliu_inform, jieliu_result, moudle3_inform, moudle3_inform_2, moudle3_result, moudle3_flag, Vc, Vcc, Vccc, Ve, Vee, Veee

    print(df['Project_inform'][0])
    import ast

    try:
        Project_inform = ast.literal_eval(df['Project_inform'][0])
    except (ValueError, SyntaxError):
        Project_inform = None

    try:
        image_base64 = df['image_base64'][0]
        if np.isnan(image_base64):
            image_base64 = None
    except (ValueError, SyntaxError):
        image_base64 = None

    try:
        jieliu_result = ast.literal_eval(df['jieliu_result'][0])
    except (ValueError, SyntaxError):
        jieliu_result = None

    try:
        moudle3_inform = ast.literal_eval(df['moudle3_inform'][0])
    except (ValueError, SyntaxError):
        moudle3_inform = None

    try:
        moudle3_inform_2 = ast.literal_eval(df['moudle3_inform_2'][0])
    except (ValueError, SyntaxError):
        moudle3_inform_2 = []

    try:
        moudle3_result = pd.read_csv(io.StringIO(df['moudle3_result'][0]), sep='\s+', header=None)
    except (ValueError, SyntaxError):
        moudle3_result = None

    moudle3_flag = df['moudle3_flag'][0]

    # 节流模块输入参数
    Qg = df['Qg'][0]
    Ql = df['Ql'][0]
    P1 = df['P1'][0]
    Pflq = df['Pflq'][0]
    T1 = df['T1'][0]
    D = df['D'][0]
    n = df['n'][0]

    n1 = df['n1'][0]
    n2 = df['n2'][0]
    n3 = df['n3'][0]
    n4 = df['n4'][0]
    L = df['L'][0]
    LL = df['LL'][0]
    LL1 = df['LL1'][0]
    LL2 = df['LL2'][0]
    LL3 = df['LL3'][0]
    r1 = df['r1'][0]
    try:
        r2 = ast.literal_eval(df['r2'][0])
    except (ValueError, SyntaxError):
        r2 = []
    Vc = '0' if df['Vc'][0] == '' else df['Vc'][0]
    Vcc = '0' if df['Vcc'][0] == '' else df['Vcc'][0]
    Vccc = '0' if df['Vccc'][0] == '' else df['Vccc'][0]
    Ve = '0' if df['Ve'][0] == '' else df['Ve'][0]
    Vee = '0' if df['Vee'][0] == '' else df['Vee'][0]
    Veee = '0' if df['Veee'][0] == '' else df['Veee'][0]
    G1 = '0' if df['G1'][0] == '' else df['G1'][0]
    G2 = '0' if df['G2'][0] == '' else df['G2'][0]
    G3 = '0' if df['G3'][0] == '' else df['G3'][0]
    P2 = '0' if df['P2'][0] == '' else df['P2'][0]
    P22 = '0' if df['P22'][0] == '' else df['P22'][0]
    P222 = '0' if df['P222'][0] == '' else df['P222'][0]
    T2 = '0' if df['T2'][0] == '' else df['T2'][0]
    T22 = '0' if df['T22'][0] == '' else df['T22'][0]
    T222 = '0' if df['T222'][0] == '' else df['T222'][0]
    try:
        Px1.append(ast.literal_eval(df['Px1_1'][0]))
        l0 = [-np.inf]
        Tx1.append(l0 + ast.literal_eval(df['Tx1_1'][0]))
        Px1.append(ast.literal_eval(df['Px1_2'][0]))
        l0 = [-np.inf]
        Tx1.append(l0 + ast.literal_eval(df['Tx1_2'][0]))
        Px1.append(ast.literal_eval(df['Px1_3'][0]))
        l0 = [-np.inf]
        Tx1.append(l0 + ast.literal_eval(df['Tx1_3'][0]))
    except (ValueError, SyntaxError) as e:
        print(e)
        Px1 = []
        Tx1 = []

    Jieliu_slot.setparameter(self)
    Jieliu_slot.setresult(self)
    compute_slot.setParameters(self)
    change_page(self, 1)


def clearData(self):
    global Project_inform, image_base64, jieliu_result, moudle3_inform, moudle3_inform_2, moudle3_result, moudle3_flag, Vc, Vcc, Vccc, Ve, Vee, Veee, Qg, Ql, P1, Pflq, T1, D, n, n1, n2, n3, n4, L, LL, LL1, LL2, LL3, r1, r2, G1, G2, G3, P2, P22, P222, T2, T22, T222, Px1, Tx1
    Project_inform = None
    image_base64 = None

    jieliu_result = None
    moudle3_inform = None
    moudle3_inform_2 = None
    moudle3_result = None
    moudle3_flag = False
    Vc = None
    Vcc = None
    Vccc = None
    Ve = None
    Vee = None
    Veee = None

    Qg = None
    Ql = None
    P1 = None
    Pflq = None
    T1 = None
    D = None
    n = None
    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    L = 0
    # LL_n1 = 0
    # LL1_n2 = 0
    # LL2_n3 = 0
    # LL3_n4 = 0
    LL = None
    LL1 = None
    LL2 = None
    LL3 = None
    r1 = None
    r2 = None
    G1 = None
    G2 = None
    G3 = None
    P2 = None
    P22 = None
    P222 = None
    T2 = None
    T22 = None
    T222 = None
    Px1 = []
    Tx1 = []
