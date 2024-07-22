import io
import os

import numpy as np
import pandas as pd

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
    global Qg, Ql, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3, r1, r2, moudle3_result
    Qg, Ql, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3, r1, r2 = Jieliu_slot.getparameter(self)
    try:
        moudle3_result.to_string(index=False, header=False)
    except AttributeError:
        moudle3_result = pd.DataFrame()
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
        'Px1_1': [str(Px1[0].tolist())],
        'Tx1_1': [str(Tx1[0].tolist())],
        'Px1_2': [str(Px1[1].tolist())],
        'Tx1_2': [str(Tx1[1].tolist())],
        'Px1_3': [str(Px1[2].tolist())],
        'Tx1_3': [str(Tx1[2].tolist())],
    })
    print(df)
    # 检查文件是否存在
    if os.path.exists(path):
        try:
            # 如果文件存在，则覆盖文件
            file = open(path, 'w')
            df.to_csv(file, index=False, mode='w')
        except PermissionError:
            print("文件被占用，请关闭文件后重试")
    else:
        # 如果文件不存在，则创建新文件
        df.to_csv(path, index=False)


def open_project(self, path):
    global Qg, Ql, P1, Pflq, T1, D, n, LL, LL1, LL2, LL3, r1, r2, moudle3_result, G1, G2, G3
    global P2,P22,P222,T2,T22,T222,Px1,Tx1
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
        moudle3_inform_2 = None

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
    LL = df['LL'][0]
    LL1 = df['LL1'][0]
    LL2 = df['LL2'][0]
    LL3 = df['LL3'][0]
    r1 = df['r1'][0]
    r2 = df['r2'][0]
    Vc = df['Vc'][0]
    Vcc = df['Vcc'][0]
    Vccc = df['Vccc'][0]
    Ve = df['Ve'][0]
    Vee = df['Vee'][0]
    Veee = df['Veee'][0]
    G1 = df['G1'][0]
    G2 = df['G2'][0]
    G3 = df['G3'][0]
    P2 = df['P2'][0]
    P22 = df['P22'][0]
    P222 = df['P222'][0]
    T2 = df['T2'][0]
    T22 = df['T22'][0]
    T222 = df['T222'][0]
    Px1.append(df['Px1_1'][0])
    Tx1.append(df['Tx1_1'][0])
    Px1.append(df['Px1_2'][0])
    Tx1.append(df['Tx1_2'][0])
    Px1.append(df['Px1_3'][0])
    Tx1.append(df['Tx1_3'][0])


    Jieliu_slot.setparameter(self)
    Jieliu_slot.setresult(self)
    compute_slot.setParameters(self)
    change_page(self, 1)
