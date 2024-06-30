import numpy as np
    
def banjing1(C = None): 
    t = np.asarray(C(:,1)).size
    ltrans = np.zeros((t,1))
    dtrans = np.zeros((t,1))
    for i in np.arange(1,t+1).reshape(-1):
        ltrans[i] = np.round(C(i,2))
        dtrans[i] = C(i,1)
    
    ##
#基础参数输入
#钻具组合参数
    Ntrans = np.asarray(dtrans).size
    
    nntrans = np.zeros((Ntrans,1))
    
    ntrans = sum(ltrans)
    
    rt = np.zeros((ntrans,1))
    
    #计算nnntrans，便于后续计算
    nntrans[1] = ltrans(1)
    for i in np.arange(2,Ntrans+1).reshape(-1):
        nntrans[i] = nntrans(i - 1) + ltrans(i)
    
    #计算钻具组合各分段的半径、截面积、线重
    for i in np.arange(1,Ntrans+1).reshape(-1):
        if i == 1:
            for j in np.arange(1,nntrans(i)+1).reshape(-1):
                rt[j] = dtrans(i) / 2
        else:
            for j in np.arange(nntrans(i - 1) + 1,nntrans(i)+1).reshape(-1):
                rt[j] = dtrans(i) / 2
    
    return rt
    
    return rt