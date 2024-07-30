import numpy as np
def Mz_func(V,LL,D,den,P):
    lamda = 0.009407 / D ** (1 / 3)  # 水力摩阻系数

    Pctiz = lamda * den * V ** 2 / 2 / 9.81 * LL / D * 1e-5  # 连续管直管段摩阻，MPa
    dertaP = np.sum(Pctiz)
    P0 = P - dertaP
    return P0, Pctiz

def Pctiz_func(V,LL,D,den):
    lamda = 0.009407 / D ** (1 / 3)  # 水力摩阻系数
    Pctiz = lamda * den * V ** 2 / 2 / 9.81 * LL / D * 1e-5  # 连续管直管段摩阻，MPa
    return Pctiz

def P0_func(Pctiz,P):
    dertaP = np.sum(Pctiz)
    P0 = P - dertaP
    return P0