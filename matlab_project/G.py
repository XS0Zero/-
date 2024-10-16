import numpy as np
import tkinter as tk
import pandas as pd
import matplotlib as mpl

from data import result_form

mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
def G_func(Qg,Ql,T1,T2,P1,P2,r):
        # 转换温度为开尔文单位
        T2 = T2 + 273.15
        a0 = 4.65295
        a1 = 3.37802E-1
        a2 = 1.11429E-2
        a3 = 2.04372E-4
        a4 = 1.91021E-6
        a5 = 1.56275E-8
        a6 = 1.99046E-10
        a7 = -1.23039E-12
        b0 = 4.67351E-2
        b1 = 4.60019E-3
        b2 = 8.68387E-6
        b3 = -4.65719E-6
        b4 = 9.32789E-8
        b5 = 2.06031E-9
        b6 = -4.79843E-11
        b7 = 2.37537E-13
        # 检查相对密度是否在合理范围内
        if r > 1 or r < 0.4:
            # 弹出错误对话框
            print("相对密度数值不正确")
            root = tk.Tk()
            root.withdraw()
            return None
            #messagebox.showerror("错误提示", "相对密度数值不正确")
        # 从 Excel 文件中读取数据
        else:
            data = pd.read_excel('resource/水合物参数.xlsx',header=None)

        # 提取数据
        Ss = data.iloc[:, 1]  # 第2列数据
        phis = data.iloc[:, 0]  # 第1列数据
        ltemp = r  # 相对密度

        # 插值计算 B 值
        from scipy.interpolate import interp1d
        B = interp1d(phis, Ss,kind='cubic')(ltemp)

        # 计算压力 Px
        T2 = T2 - 273.15
        Px = 10 ** (-1.0055 + 0.0541 * (B + T2))

        # 生成压力-温度数据
        Px1 = np.arange(0, 140, 0.0005)
        Tx1 = (np.where(Px1>0,np.log10(Px1),-np.inf) + 1.0055) / 0.0541 - B

        result_form.Px1.append(Px1)
        result_form.Tx1.append(Tx1)

        # 绘制图像

        # plt.switch_backend('Qt5Agg')
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显
        # plt.plot(Px1, Tx1, 'r')
        # plt.xlabel('压力 (MPa)', fontsize=11)
        # plt.ylabel('温度 (℃)', fontsize=11)
        # plt.title('水合物相平衡曲线')

        if P2 < Px:
            #tk.messagebox.showinfo('模拟结果',"不会生成水合物")
            print('无水合物')
            Tx = (np.where(P2>0,np.log10(P2),-np.inf) + 1.0055) / 0.0541 - B + 273
            OT = Tx - T2
            W = 70  # 注入抑制剂浓度，%
            Wr = (100 * OT * 62.07) / (2220 + OT * 62.07)  # 所需最小抑制剂浓度%
            a = (1.97E-5) * P2 ** (-0.7) * np.exp((6.054E-2) * T2 - 11.128)
            Gg = Wr * a  # 抑制剂气相用量，g/m^3

            Aa = a0 + a1 * T2 + a2 * T2 ** 2 + a3 * T2 ** 3 + a4 * T2 ** 4 + a5 * T2 ** 5 + a6 * T2 ** 6 + a7 * T2 ** 7
            Bb = b0 + b1 * T2 + b2 * T2 ** 2 + b3 * T2 ** 3 + b4 * T2 ** 4 + b5 * T2 ** 5 + b6 * T2 ** 6 + b7 * T2 ** 7
            W0 = Bb + 101.325 * Aa / (P2 * 1000)  # 节流前含水量，g/m^3
            WW = Qg * W0 / 1000  # 节流冷凝水量，kg/d
            OW = (WW + 1000 * Ql)  / Qg  # 总含水量，g/m^3
            G = 0
        else:
            print('水合物')
            Tx = (np.where(P2>0,np.log10(P2),-np.inf) + 1.0055) / 0.0541 - B + 273
            OT = Tx - T2
            W = 70  # 注入抑制剂浓度，%
            Wr = (100 * OT * 62.07) / (2220 + OT * 62.07)  # 所需最小抑制剂浓度%
            a = (1.97E-5) * P2 ** (-0.7) * np.exp((6.054E-2) * T2 - 11.128)
            Gg = Wr * a  # 抑制剂气相用量，g/m^3

            Aa = a0 + a1 * T2 + a2 * T2 ** 2 + a3 * T2 ** 3 + a4 * T2 ** 4 + a5 * T2 ** 5 + a6 * T2 ** 6 + a7 * T2 ** 7
            Bb = b0 + b1 * T2 + b2 * T2 ** 2 + b3 * T2 ** 3 + b4 * T2 ** 4 + b5 * T2 ** 5 + b6 * T2 ** 6 + b7 * T2 ** 7
            W0 = Bb + 101.325 * Aa / (P2 * 1000)  # 节流前含水量，g/m^3
            WW = Qg * W0 / 1000  # 节流冷凝水量，kg/d
            OW = (WW + 1000 * Ql) * 1000 / Qg  # 总含水量，g/m^3
            Gs = abs((OW + (100 - W) * Gg / 100) * Wr / (W - Wr))  # 抑制剂液相用量，g/m^3
            G = (Qg * (Gg + Gs) * 10E-6) / 1090  # 抑制剂总注入量，kg/d

        return G,OW,Wr,B