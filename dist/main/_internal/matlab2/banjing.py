import numpy as np
    
def banjing(C = None): 
    t = np.asarray(C(:,1)).size
    ltrans = np.zeros((t,1))
    dtrans = np.zeros((t,1))
    Dtrans = np.zeros((t,1))
    for i in np.arange(1,t+1).reshape(-1):
        ltrans[i] = np.round(C(i,3))
        dtrans[i] = C(i,1)
        Dtrans[i] = C(i,2)
    
    I = np.pi * (Dtrans(1) ** 4 - dtrans(1) ** 4) / 64
    
    ##
#基础参数输入
#钻具组合参数
    Ntrans = np.asarray(Dtrans).size
    
    nntrans = np.zeros((Ntrans,1))
    
    ntrans = sum(ltrans)
    
    Rt = np.zeros((ntrans,1))
    
    rt = np.zeros((ntrans,1))
    
    Aot = np.zeros((ntrans,1))
    
    Ait = np.zeros((ntrans,1))
    
    It = np.zeros((ntrans,1))
    
    ht = np.zeros((ntrans,1))
    
    #计算nnntrans，便于后续计算
    nntrans[1] = ltrans(1)
    for i in np.arange(2,Ntrans+1).reshape(-1):
        nntrans[i] = nntrans(i - 1) + ltrans(i)
    
    #计算钻具组合各分段的半径、截面积、线重
    for i in np.arange(1,Ntrans+1).reshape(-1):
        if i == 1:
            for j in np.arange(1,nntrans(i)+1).reshape(-1):
                Rt[j] = Dtrans(i) / 2
                rt[j] = dtrans(i) / 2
                Aot[j] = np.pi * Rt(j) ** 2
                Ait[j] = np.pi * rt(j) ** 2
                It[j] = np.pi * (Rt(j) ** 4 - rt(j) ** 4) / 4
                ht[j] = Rt(j) - rt(j)
        else:
            for j in np.arange(nntrans(i - 1) + 1,nntrans(i)+1).reshape(-1):
                Rt[j] = Dtrans(i) / 2
                rt[j] = dtrans(i) / 2
                Aot[j] = np.pi * Rt(j) ** 2
                Ait[j] = np.pi * rt(j) ** 2
                It[j] = np.pi * (Rt(j) ** 4 - rt(j) ** 4) / 4
                ht[j] = Rt(j) - rt(j)
    
    return Rt,rt,It
    
    return Rt,rt,It