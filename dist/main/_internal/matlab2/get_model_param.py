import numpy as np

from matlab2.mainfunc import pars


def get_model_param(drcs1 = None,data = None,Drcs1 = None): 
    #---------------------可变参数----------------------#
    pars.md1 = drcs1[0] / 1000
    
    pars.thyl = drcs1[2]
    
    pars.ygyl = drcs1[3]
    
    pars.Rti = drcs1[4](end()) / 2
    
    pars.DW = drcs1[4]
    pars.Rto = drcs1[5](end()) / 2
    
    pars.Rvo = np.transpose((flipud(np.transpose(drcs1[6]) / 2)))
    
    pars.Rvi = np.transpose((flipud(np.transpose(drcs1[7]) / 2)))
    
    pars.RRO = Drcs1[5] / 2
    pars.Ls = np.transpose((flipud(np.transpose(drcs1[8]))))
    pars.LS = np.transpose((flipud(np.transpose(Drcs1[4]))))
    pars.Rmax = drcs1[13]
    
    pars.Q = Drcs1[0] * 10 ** 4
    
    pars.deP = (Drcs1[2] - Drcs1[3])
    SSN = 1 - pars.deP / 100
    pars.TT = drcs1[15]
    
    pars.pint = SSN * drcs1[16]
    
    pars.rhov11 = drcs1[17]
    pars.QQ1 = drcs1[19]
    pars.fkl = drcs1[20]
    pars.LLS = drcs1[21]
    pars.fs = drcs1[22]
    
    pars.fh = drcs1[23]
    
    pars.Tint1 = drcs1[24]
    Ss,__,__,Zs,__,__ = deal_input_data(data)
    pars.DT = (pars.TT - pars.Tint1) / Zs(end())
    Zs1 = interp1(Ss,Zs,sum(pars.Ls))
    
    pars.Tint = pars.Tint1 + pars.DT * Zs1
    
    for i in np.arange(1,len(pars.rhov11)+1).reshape(-1):
        pars.rhov1[i] = pars.rhov11(i) / (np.pi * (pars.Rvo(i) ** 2 - pars.Rvi(i) ** 2))
    
    pars.rhov = mean(pars.rhov1)
    pars.NNx = drcs1[18]
    #---------------------不可变参数----------------------#
    ssd2 = len(pars.Ls)
    mesh = np.zeros((ssd2,1))
    for i in np.arange(1,ssd2+1).reshape(-1):
        mesh[i] = np.round((pars.Ls(i) / 50))
    
    pars.mesh = mesh
    
    pars.Ev = 231000000000.0
    
    pars.Ua = 6.66
    
    #   pars.Ua=23.26;              #井筒总导热系数
    pars.Zg = 1.59
    
    pars.M = 0.016
    
    #     pars.M=0.032;               #天然气摩尔质量
#     pars.cp=2227;               #天然气等压比热容
    pars.cp = 2227
    
    pars.c = 0.1
    
    pars.miuv = 0.3
    
    pars.miut = 0.3
    
    pars.ksi = 0.3
    
    pars.rhoe = 2640
    
    pars.ce = 837
    
    #   pars.ke=2.06;               #地层导热系数
    pars.ke = 2.06
    pars.Rg = 8.314
    
    pars.gama = 0.6
    
    pars.pc = 6.49
    
    pars.Tc = 190.9
    
    pars.PC = (4.666 + 0.103 * pars.gama - 0.25 * pars.gama ** 2) * 1000000.0
    
    pars.TC = 93.3 + 181 * pars.gama - 7 * pars.gama ** 2
    
    #     if  pars.gama>=0.7
#          pars.PC=(4.881-0.3861*pars.gama)*1e6;   #天然气视临界压力， Pa
#          pars.TC=92.2+176.6*pars.gama;             #天然气视临界温度， K
#     else
#          pars.PC=(4.778-0.248*pars.gama)*1e6;   #天然气视临界压力， Pa
#          pars.TC=92.2+176.6*pars.gama;             #天然气视临界温度， K
#     end
    
    pars.alphae = pars.ke / (pars.ce * pars.rhoe)
    #     pars.tD=pars.alphae/pars.Rmax^2;
#     pars.ft=0.9821*log(1+1.81*sqrt(pars.tD));
    t = 3600
    pars.tD = pars.alphae * t / pars.Rmax ** 2
    if pars.tD <= 1.5:
        pars.ft = 1.1281 * (np.sqrt(pars.tD) - 0.3 * pars.tD)
    else:
        pars.ft = (0.4036 + 0.5 * np.log(pars.tD)) * (1 + 0.6 / pars.tD)
    
    pars.im = 0.04
    
    #     pars.miu=2.555e-5;          #动力粘度
    pars.miu = 2.555e-05
    
    #计算井段流体状态的井底初始条件
    
    #     pars.rhoint=600;
    pars.rhoint = (3484.48 * pars.gama * pars.pint / 10 ** (6)) / (pars.Zg * (pars.Tint + 273))
    
    pars.wi = ((pars.Q / (24 * 60 * 60)) * 1.29 * pars.gama)
    
    #     pars.rhoint=28.96*0.77*pars.pint/pars.Zg/(pars.Tint+273)/8314;
#     pars.Vint=pars.Zg*pars.wi/(pi*pars.Rvi(end)^2)/pars.rhoint;      #井底初始流体速度
#     pars.Vint=pars.Zg*pars.wi/86400/pi/4*0.0647^2/pars.rhoint;
#     pars.Vint=5e-9*400000*pars.Zg*(pars.Tint+273)/220/0.0647^2;
    pars.Vint = 5e-09 * (pars.Q * pars.Zg * (pars.Tint + 273)) / ((pars.Rvi(end()) * 2) ** 2 * pars.pint / 10 ** (6))
    #     pars.Vint=20;
#接触力参数
    pars.khit = 1100000.0
    pars.chit = 12000.0
    
    return pars
    
    return pars