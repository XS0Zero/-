import numpy as np
import math
def MAXQd_func(den,Pflq,k,n,D):
    R0 = 478.33  # 天然气气体常数
    T0 = 293.15  # 滞止温度
    Pa = 101325  # 假定的末端压力
    # den = r * 1.2 # den = 0.72 # 标态下的天然气密度
    Vlj = 398.14  # 临界流速
    # n = 5 # 弯头数
    L = 100  # 放喷管线的长度，m
    # D = 0.06198 # 内径0.06198,m;0.1143;0.073
    Lep = 30 * D * n  # 90°弯头等效长度
    L = L + Lep  # 防喷管线长度

    A = D ** 2 * math.pi / 4
    Te = T0 * 2 / (k + 1)  # 临界温度（放喷出口处的温度）

    # Te = 191.40
    # Qd = 170
    # Pflq = 5.255e6 # 分离器工作压力（假设）
    Pq = Pflq * 1e6 / 1.25  # 安全系数

    for Qd in range(1, 1001):
        Q = Qd * 10000 / 24 / 3600  # 万方/天 -> 方/秒
        dene = den * Q / Vlj / A  # 放喷出口的天然气密度
        Pz = dene * R0 * Te  # 放喷管线出口终点压力

        P = 2 / 3 * (Pq + Pz ** 2 / (Pq + Pz)) / 1000000  # 天然气的平均压力
        Z = 100 / (100 + 2.916 * P ** 1.25)  # 压缩系数

        lamda = 0.009407 / D ** (1 / 3)  # 水力摩阻系数
        M2 = ((Pq ** 2 - Pz ** 2) * A ** 2 / Z / R0 / T0 / (lamda * L / D + 2 * np.log(Pq / Pz))) ** 0.5  # 天然气的质量流量
        Q2 = M2 / dene  # 体积流量
        Qd2 = Q2 * 24 * 3600 / 10000  # 万方/天

        if Qd > Qd2:
            break

    Qd = Qd * 10 ^ 4

    return Qd