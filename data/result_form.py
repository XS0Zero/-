import io
import os

import numpy as np
import pandas as pd

from ctrl import Jieliu_slot, compute_slot
from ctrl.menu_slot import change_page

Project_inform = None
image_base64 = None
jieliu_inform = None
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

def save_project(path):
    df = pd.DataFrame({
        'Project_inform': [Project_inform],
        'image_base64': [image_base64],
        'jieliu_inform': [jieliu_inform],
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
        'Veee': [Veee]
    })
    print(df)
    # 检查文件是否存在
    if os.path.exists(path):
        try:
            # 如果文件存在，则覆盖文件
            file = open(path,'w')
            df.to_csv(file, index=False, mode='w')
        except PermissionError:
            print("文件被占用，请关闭文件后重试")
    else:
        # 如果文件不存在，则创建新文件
        df.to_csv(path, index=False)

def open_project(self,path):
    try:
        df = pd.read_csv(path,encoding='gbk')
    except UnicodeDecodeError:
        df = pd.read_csv(path,encoding='utf-8')
    print(df)

    global Project_inform, image_base64, jieliu_inform, jieliu_result, moudle3_inform,moudle3_inform_2, moudle3_result, moudle3_flag, Vc, Vcc, Vccc, Ve, Vee, Veee

    print(df['Project_inform'][0])
    import ast

    try:
        Project_inform = ast.literal_eval(df['Project_inform'][0])
    except (ValueError, SyntaxError):
        Project_inform = None

    try:
        image_base64 = df['image_base64'][0]
    except (ValueError, SyntaxError):
        image_base64 = None

    try:
        jieliu_inform = ast.literal_eval(df['jieliu_inform'][0])
    except (ValueError, SyntaxError):
        jieliu_inform = None

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
        moudle3_result = pd.read_csv(io.StringIO(df['moudle3_result'][0]),sep='\s+',header=False)
    except (ValueError, SyntaxError):
        moudle3_result = None

    moudle3_flag = df['moudle3_flag'][0]

    Vc = df['Vc'][0]
    Vcc = df['Vcc'][0]
    Vccc = df['Vccc'][0]
    Ve = df['Ve'][0]
    Vee = df['Vee'][0]
    Veee = df['Veee'][0]

    Jieliu_slot.setparameter(self)
    Jieliu_slot.setresult(self)
    compute_slot.setParameters(self)
    change_page(self, 1)

