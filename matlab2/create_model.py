import numpy as np
    
def create_model(Vz = None,rho0z = None,state_z = None,pars = None,Ss = None,Xs = None,Ys = None,Zs = None,alphas = None,phis = None): 
    #划分单元计算单元各个节点坐标以及各个单元节点对应的长度位置，井斜角，方位角，油管内径，油管外径
    nodes = create_mesh(pars,Ss,Xs,Ys,Zs,alphas,phis)
    
    
    nelem = sum(pars.mesh)
    
    Kgg = np.zeros(((nelem + 1) * 5,(nelem + 1) * 5))
    Mgg = np.zeros(((nelem + 1) * 5,(nelem + 1) * 5))
    Cgg = np.zeros(((nelem + 1) * 5,(nelem + 1) * 5))
    Fgravg = np.zeros(((nelem + 1) * 5,1))
    transmat = cell(nelem,1)
    
    #循环计算单元刚度质量阻尼矩阵并组装
#形函数:单元坐标系下节点自由度顺序为：z,x,ry,y,rx
    phix = lambda z = None,le = None: np.array([[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[z - 2 * z ** 2 / le + z ** 3 / le ** 2],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- z ** 2 / le + z ** 3 / le ** 2],[0],[0]])
    phiy = lambda z = None,le = None: np.array([[0],[0],[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[- (z - 2 * z ** 2 / le + z ** 3 / le ** 2)],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- (- z ** 2 / le + z ** 3 / le ** 2)]])
    phiz = lambda z = None,le = None: np.array([[1 - z / le],[0],[0],[0],[0],[z / le],[0],[0],[0],[0]])
    #采用差分方式定义一阶微分
    scale = 0.01
    
    dphix = lambda z = None,le = None: (phix(z + scale,le) - phix(z - scale,le)) / 2 / scale
    ddphix = lambda z = None,le = None: (dphix(z + scale,le) - dphix(z - scale,le)) / 2 / scale
    dphiy = lambda z = None,le = None: (phiy(z + scale,le) - phiy(z - scale,le)) / 2 / scale
    ddphiy = lambda z = None,le = None: (dphiy(z + scale,le) - dphiy(z - scale,le)) / 2 / scale
    dphiz = lambda z = None,le = None: (phiz(z + scale,le) - phiz(z - scale,le)) / 2 / scale
    ddphiz = lambda z = None,le = None: (dphiz(z + scale,le) - dphiz(z - scale,le)) / 2 / scale
    #       dphix=@(z,le)[0;-6*z/le^2+6*z^2/le^3;1-4*z/le+3*z^2/le^2;0;0;0;6*z/le^2-6*z^2/le^3;-2*z/le+3*z^2/le^2;0;0];
#       ddphix=@(z,le)[0;-6/le^2+12*z/le^3;-4/le+6*z/le^2;0;0;0;6/le^2-12*z/le^3;-2/le+6*z/le^2;0;0];
#       dphiy=@(z,le)[0;0;0;-6*z/le^2+6*z^2/le^3;1-4*z/le+3*z^2/le^2;0;0;0;6*z/le^2-6*z^2/le^3;-2*z/le+3*z^2/le^2];
#       ddphiy=@(z,le)[0;0;0;-6/le^2+12*z/le^3;-4/le+6*z/le^2;0;0;0;6/le^2-12*z/le^3;-2/le+6*z/le^2];
#       dphiz=@(z,le)[-1/le;0;0;0;0;1/le;0;0;0;0];
#       ddphiz=@(z,le)[0;0;0;0;0;0;0;0;0;0];
    
    for i in np.arange(1,nelem+1).reshape(-1):
        #生成单元坐标系下的质量刚度阻尼矩阵
        M,K,C,fgrave,elem_transmat,A11,A22,le1,I11,I21 = create_elem_mat_in_local(nodes(i,:),nodes(i + 1,:),pars,phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,state_z,rho0z,Vz)
        #组装刚度质量阻尼矩阵
        A1[i] = A11
        A2[i] = A22
        le[i] = le1
        I1[i] = I11
        I2[i] = I21
        Kgg[np.arange[i * 5 - 4,i * 5 + 5+1],np.arange[i * 5 - 4,i * 5 + 5+1]] = Kgg(np.arange(i * 5 - 4,i * 5 + 5+1),np.arange(i * 5 - 4,i * 5 + 5+1)) + np.transpose(elem_transmat) * K * elem_transmat
        Mgg[np.arange[i * 5 - 4,i * 5 + 5+1],np.arange[i * 5 - 4,i * 5 + 5+1]] = Mgg(np.arange(i * 5 - 4,i * 5 + 5+1),np.arange(i * 5 - 4,i * 5 + 5+1)) + np.transpose(elem_transmat) * M * elem_transmat
        Cgg[np.arange[i * 5 - 4,i * 5 + 5+1],np.arange[i * 5 - 4,i * 5 + 5+1]] = Cgg(np.arange(i * 5 - 4,i * 5 + 5+1),np.arange(i * 5 - 4,i * 5 + 5+1)) + np.transpose(elem_transmat) * C * elem_transmat
        #         Fgravg(i*5-4:i*5+5)=Fgravg(i*5-4:i*5+5)+elem_transmat'*fgrave;
        Fgravg[np.arange[i * 5 - 4,i * 5 + 5+1]] = Fgravg(np.arange(i * 5 - 4,i * 5 + 5+1)) + fgrave
        transmat[i] = elem_transmat
    
    return Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2
    
    
def create_mesh(pars = None,Ss = None,Xs = None,Ys = None,Zs = None,alphas = None,phis = None): 
    nodes = np.zeros((sum(pars.mesh),9))
    ltemp = 0
    count = 2
    for i in np.arange(1,np.asarray(pars.mesh).size+1).reshape(-1):
        le = pars.Ls(i) / pars.mesh(i)
        for j in np.arange(1,pars.mesh(i)+1).reshape(-1):
            ltemp = ltemp + le
            x0 = interp1(Ss,Xs,ltemp,'spline')
            y0 = interp1(Ss,Ys,ltemp,'spline')
            z0 = interp1(Ss,Zs,ltemp,'spline')
            alpha0 = interp1(Ss,alphas,ltemp,'spline')
            phi0 = interp1(Ss,phis,ltemp,'spline')
            nodes[count,:] = np.array([x0,y0,z0,ltemp,alpha0,phi0,pars.Rvi(i),pars.Rvo(i),pars.QQ1(i)])
            count = count + 1
    
    return nodes
    
    
def create_elem_mat_in_local(node1 = None,node2 = None,pars = None,phix = None,phiy = None,phiz = None,dphix = None,dphiy = None,dphiz = None,ddphix = None,ddphiy = None,ddphiz = None,state_z = None,rho0z = None,Vz = None): 
    #计算一些参数
    le = norm(node2(np.arange(1,3+1)) - node1(np.arange(1,3+1)),2)
    
    A1 = np.pi * node1(8) ** 2 - np.pi * node1(7) ** 2
    A2 = np.pi * node2(8) ** 2 - np.pi * node2(7) ** 2
    
    I1 = np.pi * node1(8) ** 4 / 4 - np.pi * node1(7) ** 4 / 4
    I2 = np.pi * node2(8) ** 4 / 4 - np.pi * node2(7) ** 4 / 4
    
    I = lambda z = None: interp1(np.array([0,le]),np.array([I1,I2]),z)
    
    A = lambda z = None: interp1(np.array([0,le]),np.array([A1,A2]),z)
    
    ve = 1 / 3 * le * (A1 + np.sqrt(A1 * A2) + A2)
    
    mv = pars.rhov * ve
    
    rho0 = lambda z = None,le = None: interp1(state_z,rho0z,node1(3) + (node2(3) - node1(3)) * z / le,'spline')
    
    Aempty = lambda z = None: interp1(np.array([0,le]),np.pi * pars.Rti ** 2 - np.pi * np.array([node1(8) ** 2,node2(8) ** 2]),z)
    
    m0 = quadgk(lambda z = None: np.multiply(rho0(z,le),Aempty(z)),0,le)
    V = quadgk(lambda z = None: Aempty(z),0,le)
    
    #计算单元质量矩阵
    M1 = quadv(lambda z = None: (mv + m0) * phix(z,le) * np.transpose((phix(z,le))),0,le)
    
    M2 = quadv(lambda z = None: (mv + m0) * phiy(z,le) * np.transpose((phiy(z,le))),0,le)
    
    M3 = quadv(lambda z = None: (pars.rhov * I(z)) * dphix(z,le) * np.transpose((dphix(z,le))),0,le)
    
    M4 = quadv(lambda z = None: (pars.rhov * I(z)) * dphiy(z,le) * np.transpose((dphiy(z,le))),0,le)
    
    M5 = quadv(lambda z = None: mv * phiz(z,le) * np.transpose((phiz(z,le))),0,le)
    
    M = M1 + M2 + M3 + M4 + M5
    #计算单元阻尼矩阵
    C1 = quadv(lambda z = None: pars.c * phix(z,le) * np.transpose((phix(z,le))),0,le)
    
    C2 = quadv(lambda z = None: 2 * m0 * V * phix(z,le) * np.transpose((dphix(z,le))),0,le)
    
    C3 = quadv(lambda z = None: pars.c * phiy(z,le) * np.transpose((phiy(z,le))),0,le)
    
    C4 = quadv(lambda z = None: 2 * m0 * V * phiy(z,le) * np.transpose((dphiy(z,le))),0,le)
    
    C5 = quadv(lambda z = None: pars.c * phiz(z,le) * np.transpose((phiz(z,le))),0,le)
    
    C = C1 + C2 + C3 + C4 + C5
    #计算单元刚度矩阵,其他刚度矩阵在迭代中更新
    K1 = quadv(lambda z = None: pars.Ev * I(z) * ddphix(z,le) * np.transpose((ddphix(z,le))),0,le)
    
    K2 = quadv(lambda z = None: pars.Ev * I(z) * ddphiy(z,le) * np.transpose((ddphiy(z,le))),0,le)
    
    K3 = quadv(lambda z = None: - m0 * V ** 2 * dphix(z,le) * np.transpose((dphix(z,le))),0,le)
    
    K4 = quadv(lambda z = None: - m0 * V ** 2 * dphiy(z,le) * np.transpose((dphiy(z,le))),0,le)
    
    K11 = quadv(lambda z = None: pars.Ev * A(z) * dphiz(z,le) * np.transpose((dphiz(z,le))),0,le)
    
    K = K1 + K2 + K3 + K4 + K11
    #计算单元坐标变换矩阵
#采用单元中部的井斜角和方位角
    alpha = (node1(5) + node2(5)) / 2
    phi = (node1(6) + node2(6)) / 2
    #     T1=[cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0;##有可能有问题
#         sin(alpha),cos(alpha),0,0,0;
#         0,0,1,0,0;
#         -cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0;
#         0,0,0,0,1];
#     elem_transmat=[cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0,0,0,0,0,0;
#         sin(alpha),cos(alpha),0,0,0,0,0,0,0,0;
#         0,0,1,0,0,0,0,0,0,0;
#         -cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0,0,0,0,0,0;
#         0,0,0,0,1,0,0,0,0,0,;
#         0,0,0,0,0,cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0;
#         0,0,0,0,0,sin(alpha),cos(alpha),0,0,0;
#         0,0,0,0,0,0,0,1,0,0;
#         0,0,0,0,0,-cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0;
#         0,0,0,0,0,0,0,0,0,1];
    T1 = np.array([[np.cos(alpha),- np.sin(phi) * np.sin(alpha),0,np.sin(alpha) * np.cos(phi),0],[0,np.cos(phi),0,np.sin(phi),0],[0,0,1,0,0],[- np.sin(alpha),- np.sin(phi) * np.cos(alpha),0,np.cos(alpha) * np.cos(phi),0],[0,0,0,0,1]])
    elem_transmat = blkdiag(T1,T1)
    #重力
    thetad = (node1(5) + node2(5)) / 2
    q = quadgk(lambda z = None: np.multiply((pars.rhov - rho0(z,le)),A(z)) * 9.81,0,le)
    
    #      q1=q*cos(thetad);         #重力在求解坐标系分量
#      q2=q*sin(thetad);
#      fgrave=-[-q1*le/2,-q2*le/2,0,0,-q2*le^2/12,-q1*le/2,-q2*le/2,0,0,q1*le^2/12]';
    fgrave = np.transpose(np.array([q / 2,0,0,0,0,q / 2,0,0,0,0]))
    #      fgrave=0;
    
    return M,K,C,fgrave,elem_transmat,A1,A2,le,I1,I2
    
    return Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2