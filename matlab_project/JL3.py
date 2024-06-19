import numpy as np
from BWRSV1 import BWRSV1_func
def JL_func(P1,T1,Qg,r,k,R,Pc,Tc,Pci,Tci):
    T1 = T1 + 273.15
    Pr1 = P1 / Pc  # 节流前拟对比压力
    Tr1 = T1 / Tc  # 节流前拟对比温度
    Z1 = BWRSV1_func(P1, T1)[0]  # 调用BWRSV1函数计算压缩因子
    a0 = (2 / (k + 1)) ** (2 / (k - 1)) - (2 / (k + 1)) ** ((k + 1) / (k - 1))
    b0 = k / (k - 1)

    d1 = ((Qg / 10000) * (r * T1 * Z1) ** 0.5 / 0.4066 / P1 / (a0 * b0) ** 0.5) ** 0.5
    ff=(2 / (k + 1) )** (k / (k - 1)) * P1
    for P2 in np.arange(0.1,( 2 / (k + 1)) ** (k / (k - 1)) * P1, 0.01):
        a = (P2 / P1) ** (2 / k) - (P2 / P1) ** ((k + 1) / k)
        b = k / (k - 1)
        Qg1 = 0.408 * P1 * d1 ** 2 * (a * b) ** 0.5 * 10000 / ((r * T1 * Z1) ** 0.5)
        Cp = 13.19 + 0.09224 * (T1 - 14) - (T1 - 14) ** 2 * 0.00006238 + 0.9965 * 29.16 * r * (
                    5 * (P1 + P2)) ** 1.124 / ((T1 - 14) / 100) ** 5.08
        # Cp = 12.43 + 3.14*(T1)*1e-2 + 7.931*(T1)**2*1e-4 - 6.881*(T1)**3*1e-7
        w = 0.013  # 甲烷偏心因子
        m = 0.48 + 1.574 * w - 0.176 * w ** 2
        beta = (1 + m * (1 - Tr1 ** 0.5)) ** 2
        ra = 0.42747 * beta * Tci ** 2 / Pci
        rb = 0.08664 * Cp * Tci / Pci
        A = ra * P1 / T1
        B = rb * P1 / T1
        f = 2.343 * ((T1 - 38) / Tci) ** (-2.04) - 0.071 * ((P1 + P2) / (2 * Pci) - 0.8)
        Cj = Tci * f * 4.1868 / (Pci * Cp)
        # Cj = r/Cp*((2*ra-rb*(T1)-2*rb*B*(T1))*Z1-(2*ra*B+rb*A*(T1)))/(3*Z1**2-2*Z1+A-B-B**2)/(T1)
        DertaT = Cj * (P1 - P2)
        T2 = T1 - DertaT - 273.15  # 将温度从开尔文转换回摄氏度
        if Qg1 >= Qg:
            break
        d=d1

    return P2, T2, d, Qg1, Z1
