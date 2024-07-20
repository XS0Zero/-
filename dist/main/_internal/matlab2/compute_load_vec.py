import numpy as np
import matplotlib.pyplot as plt
    
def compute_load_vec(dofg = None,nodes = None,pars = None,Ugt = None,Vgt = None,transmat = None,Vz = None,rho0z = None,state_z = None,DDW1 = None): 
    #计算管柱的受力，包括流体力和壁面接触力
    
    #计算流体作用力
    Fv,Fv1 = create_flow_force(dofg,nodes,Ugt,pars,transmat,Vz,rho0z,state_z)
    #计算接触力
    Fcontact,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt = create_contact_force(dofg,nodes,Ugt,Vgt,pars,transmat,DDW1)
    #综合
    Fg = Fv + Fcontact
    return Fg,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt,Fv1
    
    
def create_flow_force(dofg = None,nodes = None,Ugt = None,pars = None,transmat = None,Vz = None,rho0z = None,state_z = None): 
    Fv = np.zeros((dofg,1))
    nelem = sum(pars.mesh)
    Fv1 = np.zeros((dofg / 5,1))
    #插值函数
    phix = lambda z = None,le = None: np.array([[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[z - 2 * z ** 2 / le + z ** 3 / le ** 2],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- z ** 2 / le + z ** 3 / le ** 2],[0],[0]])
    phiy = lambda z = None,le = None: np.array([[0],[0],[0],[1 - 3 * z ** 2 / le ** 2 + 2 * z ** 3 / le ** 3],[- (z - 2 * z ** 2 / le + z ** 3 / le ** 2)],[0],[0],[0],[3 * z ** 2 / le ** 2 - 2 * z ** 3 / le ** 3],[- (- z ** 2 / le + z ** 3 / le ** 2)]])
    for i in np.arange(1,nelem+1).reshape(-1):
        Ue = Ugt(np.arange(i * 5 - 4,i * 5 + 5+1))
        ue = transmat[i] * Ue
        z1 = nodes(i,3)
        z2 = nodes(i + 1,3)
        #单元长度
        le = nodes(i + 1,4) - nodes(i,4)
        #计算单元中部所在垂深的流体密度和流速
        zzs = np.round((z1 + z2) / 2)
        rho0 = rho0z(zzs)
        V = Vz(zzs)
        #         rho0=interp1(state_z,rho0z,(z1+z2)/2,'spline');
#         V=interp1(state_z,Vz,(z1+z2)/2,'spline');
#单元截面积，两个节点平均
        A0 = ((np.pi * nodes(i,8) ** 2 - np.pi * nodes(i,7) ** 2) + (np.pi * nodes(i + 1,8) ** 2 - np.pi * nodes(i + 1,7) ** 2)) / 2
        #单元两个节点位置的井斜角方位角，考虑变形附加
        alpha1 = nodes(i,5) + ue(3)
        alpha2 = nodes(i + 1,5) + ue(8)
        phi1 = nodes(i,6) + ue(5)
        phi2 = nodes(i + 1,6) + ue(10)
        if np.abs(phi1 - phi2) <= np.pi:
            detphi = (phi2 - phi1)
        else:
            if phi1 > phi2:
                detphi = - np.abs((2 * np.pi - phi1) + phi2)
            else:
                if phi2 > phi1:
                    detphi = np.abs((2 * np.pi - phi2) + phi1)
        Fx = - rho0 * A0 * V ** 2 * np.sin(alpha2 - alpha1) * np.cos(detphi)
        Fy = - rho0 * A0 * V ** 2 * np.sin(alpha2 - alpha1) * np.sin(detphi)
        Fz = - rho0 * A0 * V ** 2 * np.cos(alpha2 - alpha1)
        #         Fx=0;
#         Fy=0;
#         Fz=0;
#载荷作为集中载荷作用在单元中部，计算其单元坐标系下等效节点力
        phiz = lambda z = None,le = None: np.array([[1 - z / le],[0],[0],[0],[0],[z / le],[0],[0],[0],[0]])
        fe = phix(le / 2,le) * Fx + phiy(le / 2,le) * Fy + phiz(le / 2,le) * Fz
        #         Fe=transmat{i}'*fe;          #变换到全局坐标系
        Fv[np.arange[i * 5 - 4,i * 5 + 5+1]] = Fv(np.arange(i * 5 - 4,i * 5 + 5+1)) + fe
        Fv1[i] = Fv((i - 1) * 5 + 6)
    
    return Fv,Fv1
    
    
def create_contact_force(dofg = None,nodes = None,Ugt = None,Vgt = None,pars = None,transmat = None,DDW1 = None): 
    Fcontact = np.zeros((dofg,1))
    uxgt = np.zeros((dofg / 5,1))
    uygt = np.zeros((dofg / 5,1))
    uzgt = np.zeros((dofg / 5,1))
    Nxt = np.zeros((dofg / 5 - 1,1))
    Fxt = np.zeros((dofg / 5,1))
    Fyt = np.zeros((dofg / 5,1))
    Fnt = np.zeros((dofg / 5,1))
    for i in np.arange(2,nodes.shape[1-1]+1).reshape(-1):
        #计算单元坐标系下节点的位移和速度
        Ue = Ugt(np.arange((i - 2) * 5 + 1,(i - 1) * 5 + 5+1))
        ue = transmat[i - 1] * Ue
        #提取节点三个方向位移
        uxgt[i] = ue(7)
        uygt[i] = ue(9)
        uzgt[i] = ue(6)
        ux = ue(7)
        uy = ue(9)
        Ve = Vgt(np.arange((i - 2) * 5 + 1,(i - 1) * 5 + 5+1))
        ve = transmat[i - 1] * Ve
        vx = ve(7)
        vy = ve(9)
        #计算接触变形
        R1 = (nodes(i,8))
        R2 = DDW1(i)
        delta = np.sqrt(ux ** 2 + uy ** 2) - (R2 - R1)
        if delta > 0:
            #法向接触速度
            vvec = np.array([[vx],[vy]])
            uvec = np.array([[ux],[uy]])
            vn = np.transpose(vvec) * uvec / norm(uvec,2)
            vnvec = vn * uvec / norm(uvec,2)
            vtvec = vvec - vnvec
            #计算法向接触力和切向摩擦力
            Fn = pars.khit * delta ** 1.5 + pars.chit * vn * (vn > 0)
            Ft = Fn * pars.ksi
            #载荷在x,y方向投影
            Fxy = - np.array([[Fn * uvec(1) / norm(uvec,2)],[Fn * uvec(2) / norm(uvec,2)]]) - np.array([[Ft * vtvec(1) / norm(vtvec,2)],[Ft * vtvec(2) / norm(vtvec,2)]])
            #单元坐标系下载荷
#             fe=[0;0;0;0;0;Ft;Fxy(1);0;Fxy(2);0];
            fe = np.array([[0],[0],[0],[0],[0],[0],[Fxy(1)],[0],[Fxy(2)],[0]])
            Fcontact[np.arange[[i - 2] * 5 + 1,[i - 1] * 5 + 5+1]] = Fcontact(np.arange((i - 2) * 5 + 1,(i - 1) * 5 + 5+1)) + np.transpose(transmat[i - 1]) * fe
            #提取接触力
            Fxt[i] = Fxy(1)
            Fyt[i] = Fxy(2)
            Fnt[i] = Fn
            #plot_state(R2-R1,ux,uy,45,i);
        #计算单元轴向力
        A1 = np.pi * nodes(i - 1,8) ** 2 - np.pi * nodes(i - 1,7) ** 2
        A2 = np.pi * nodes(i,8) ** 2 - np.pi * nodes(i,7) ** 2
        le = norm(nodes(i,np.arange(1,3+1)) - nodes(i - 1,np.arange(1,3+1)),2)
        Nxt[i - 1] = (ue(6) - ue(1)) * pars.Ev * (A1 + A2) / 2 / le
    
    return Fcontact,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt
    
    
def plot_state(R = None,ux = None,uy = None,select_node = None,nowpoint = None): 
    if nowpoint != select_node:
        return
    
    theta = np.arange(0,2 * np.pi+0.01,0.01)
    plt.figure(100)
    plt.plot(R * np.cos(theta),R * np.sin(theta),'r')
    hold('on')
    scatter(ux,uy)
    hold('off')
    pause(0.0001)
    return
    
    return Fg,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt,Fv1