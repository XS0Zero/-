import numpy as np
    
def create_timevary_stiff(Ugt = None,transmat = None,nodes = None,pars = None): 
    #计算时变刚度矩阵
#形函数:单元坐标系下节点自由度顺序为：z,x,ry,y,rx
    phix = lambda z = None,le = None: np.array([[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[z - 2 * z ** 2 / le + z ** 3 / le ** 2],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- z ** 2 / le + z ** 3 / le ** 2],[0],[0]])
    phiy = lambda z = None,le = None: np.array([[0],[0],[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[- (z - 2 * z ** 2 / le + z ** 3 / le ** 2)],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- (- z ** 2 / le + z ** 3 / le ** 2)]])
    phiz = lambda z = None,le = None: np.array([[1 - z / le],[0],[0],[0],[0],[z / le],[0],[0],[0],[0]])
    #采用差分方式定义一阶微分,二阶微分
    scale = 0.01
    
    dphix = lambda z = None,le = None: (phix(z + scale,le) - phix(z - scale,le)) / 2 / scale
    ddphix = lambda z = None,le = None: (dphix(z + scale,le) - dphix(z - scale,le)) / 2 / scale
    dphiy = lambda z = None,le = None: (phiy(z + scale,le) - phiy(z - scale,le)) / 2 / scale
    ddphiy = lambda z = None,le = None: (dphiy(z + scale,le) - dphiy(z - scale,le)) / 2 / scale
    dphiz = lambda z = None,le = None: (phiz(z + scale,le) - phiz(z - scale,le)) / 2 / scale
    ddphiz = lambda z = None,le = None: (dphiz(z + scale,le) - dphiz(z - scale,le)) / 2 / scale
    nelem = sum(pars.mesh)
    Kggadd = np.zeros(((nelem + 1) * 5,(nelem + 1) * 5))
    for i in np.arange(1,nelem+1).reshape(-1):
        Kadd = create_elem_timevary_stiff_in_local(nodes(i,:),nodes(i + 1,:),pars,phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,Ugt(np.arange(i * 5 - 4,i * 5 + 5+1)),transmat[i])
        #组装附加刚度矩阵
        Kggadd[np.arange[i * 5 - 4,i * 5 + 5+1],np.arange[i * 5 - 4,i * 5 + 5+1]] = Kggadd(np.arange(i * 5 - 4,i * 5 + 5+1),np.arange(i * 5 - 4,i * 5 + 5+1)) + np.transpose(transmat[i]) * Kadd * transmat[i]
    
    return Kggadd
    
    
def create_elem_timevary_stiff_in_local(node1 = None,node2 = None,pars = None,phix = None,phiy = None,phiz = None,dphix = None,dphiy = None,dphiz = None,ddphix = None,ddphiy = None,ddphiz = None,Uet = None,elem_transmat = None): 
    
    #计算一些参数
    le = norm(node2(np.arange(1,3+1)) - node1(np.arange(1,3+1)),2)
    
    A1 = np.pi * node1(8) ** 2 - np.pi * node1(7) ** 2
    A2 = np.pi * node2(8) ** 2 - np.pi * node2(7) ** 2
    
    I1 = np.pi * node1(8) ** 4 / 4 - np.pi * node1(7) ** 4 / 4
    I2 = np.pi * node2(8) ** 4 / 4 - np.pi * node2(7) ** 4 / 4
    
    I = lambda z = None: interp1(np.array([0,le]),np.array([I1,I2]),z)
    
    A = lambda z = None: interp1(np.array([0,le]),np.array([A1,A2]),z)
    
    uet = elem_transmat * Uet
    
    K5 = quadv(lambda z = None: pars.Ev * A(z) * dphix(z,le) * np.transpose(uet) * (dphiz(z,le)) * np.transpose((phix(z,le))),0,le)
    
    K6 = quadv(lambda z = None: pars.Ev * A(z) * dphiy(z,le) * np.transpose(uet) * (dphiz(z,le)) * np.transpose((dphiy(z,le))),0,le)
    
    K7 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphix(z,le) * np.transpose((dphix(z,le))) * uet * np.transpose(uet) * phix(z,le) * np.transpose((phix(z,le))),0,le)
    
    K8 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphiy(z,le) * np.transpose((dphiy(z,le))) * uet * np.transpose(uet) * dphiy(z,le) * np.transpose((dphiy(z,le))),0,le)
    
    K9 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphix(z,le) * np.transpose((dphix(z,le))) * uet * np.transpose(uet) * dphiy(z,le) * np.transpose((dphiy(z,le))),0,le)
    
    K10 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphiy(z,le) * np.transpose((dphiy(z,le))) * uet * np.transpose(uet) * dphix(z,le) * np.transpose((dphix(z,le))),0,le)
    
    K12 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphiz(z,le) * np.transpose((dphix(z,le))) * uet * np.transpose((dphix(z,le))),0,le)
    
    K13 = quadv(lambda z = None: 1 / 2 * pars.Ev * A(z) * dphiz(z,le) * np.transpose((dphiy(z,le))) * uet * np.transpose((dphiy(z,le))),0,le)
    
    Kadd = K5 + K6 + K7 + K8 + K9 + K10 + K12 + K13
    return Kadd
    
    return Kggadd