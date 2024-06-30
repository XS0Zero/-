import numpy as np
    
def create_hit_load(Ug = None,Vg = None,kh = None,kh0 = None,cf = None,miud = None,miudx = None,rs = None,Ri = None,meshs = None,trans_mat = None): 
    uy = np.zeros((sum(meshs) + 1,1))
    uz = np.zeros((sum(meshs) + 1,1))
    vx = np.zeros((sum(meshs) + 1,1))
    vy = np.zeros((sum(meshs) + 1,1))
    vz = np.zeros((sum(meshs) + 1,1))
    vt = np.zeros((sum(meshs) + 1,1))
    for i in np.arange(1,sum(meshs)+1).reshape(-1):
        R = Ri
        Ue = Ug(np.arange(i * 5 - 4,i * 5 + 5+1))
        Ve = Vg(np.arange(i * 5 - 4,i * 5 + 5+1))
        Ue = trans_mat[i] * Ue
        Ve = trans_mat[i] * Ve
        uy[i] = uy(i) + Ue(4)
        uy[i + 1] = uy(i + 1) + Ue(9)
        uz[i] = uz(i) + Ue(1)
        uz[i + 1] = uz(i + 1) + Ue(6)
        vx[i] = vx(i) + Ve(2)
        vx[i + 1] = vx(i + 1) + Ve(7)
        vy[i] = vy(i) + Ve(4)
        vy[i + 1] = vy(i + 1) + Ve(9)
        vz[i] = vz(i) + Ve(1)
        vz[i + 1] = vz(i + 1) + Ve(6)
        vt[i] = 0
        vt[i + 1] = 0
    
    uy[np.arange[2,end() - 1+1]] = uy(np.arange(2,end() - 1+1)) / 2
    uz[np.arange[2,end() - 1+1]] = uz(np.arange(2,end() - 1+1)) / 2
    vx[np.arange[2,end() - 1+1]] = vx(np.arange(2,end() - 1+1)) / 2
    vy[np.arange[2,end() - 1+1]] = vy(np.arange(2,end() - 1+1)) / 2
    vz[np.arange[2,end() - 1+1]] = vz(np.arange(2,end() - 1+1)) / 2
    vt[np.arange[2,end() - 1+1]] = vt(np.arange(2,end() - 1+1)) / 2
    ur = np.sqrt(uy ** 2 + uz ** 2)
    dur = np.sqrt(vy ** 2 + vz ** 2)
    #构建钻柱外径向量
    r = np.zeros((uy.shape,uy.shape))
    r[1] = rs(1)
    count = 1
    for i in np.arange(1,np.asarray(meshs).size+1).reshape(-1):
        r[np.arange[count + 1,count + meshs[i]+1]] = rs(i)
        count = count + meshs(i)
    
    Ff = np.zeros((vy.shape,vy.shape))
    Fy = Ff
    Fz = Ff
    
    Fx = Ff
    cosall = np.multiply(np.array([uy,uz]),np.array([vy,vz]))
    cosall = (cosall(:,1) + cosall(:,2)) / ur
    Fn = np.multiply((- (ur + r - R) * kh - np.multiply(dur * cf,cosall)),(ur + r - R >= 0))
    
    Fn[1] = np.multiply((- (ur(1) + r(1) - R(1)) * kh0 - np.multiply(dur(1) * cf,cosall(1))),(ur(1) + r(1) - R(1) >= 0))
    
    loc = find(ur + r - R >= 0)
    if np.asarray(loc).size != 0:
        Ff[loc] = np.multiply(- np.abs(miud * Fn(loc)),np.sign(vt(loc)))
        Fx[loc] = np.multiply(- np.abs(miudx * Fn(loc)),np.sign(vx(loc)))
        Fy[loc] = np.multiply(Fn(loc),uy(loc)) / (uy(loc) ** 2 + uz(loc) ** 2) + np.multiply(Ff(loc),uz(loc)) / (uy(loc) ** 2 + uz(loc) ** 2)
        Fz[loc] = np.multiply(Fn(loc),uz(loc)) / (uy(loc) ** 2 + uz(loc) ** 2) + np.multiply(Ff(loc),uy(loc)) / (uy(loc) ** 2 + uz(loc) ** 2)
    
    Fhit = np.zeros((Ug.shape,Ug.shape))
    
    Fhit[np.arange[2,end()+5,5]] = Fx
    Fhit[np.arange[4,end()+5,5]] = Fy
    Fhit[np.arange[1,end()+5,5]] = Fz
    #碰撞摩擦力等效载荷
    FhitG = np.zeros((Fhit.shape,Fhit.shape))
    
    for i in np.arange(1,sum(meshs)+1).reshape(-1):
        Fe = Fhit(np.arange(i * 5 - 4,i * 5 + 5+1))
        Fhit[np.arange[i * 5 - 4,i * 5 + 5+1]] = 0
        FhitG[np.arange[i * 5 - 4,i * 5 + 5+1]] = FhitG(np.arange(i * 5 - 4,i * 5 + 5+1)) + np.transpose((trans_mat[i])) * Fe
    
    return FhitG
    
    return FhitG