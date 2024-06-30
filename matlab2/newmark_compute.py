import numpy as np
    
def newmark_compute(dt = None,time = None,Mgg = None,Kgg = None,Cgg = None,Fgravg = None,transmat = None,nodes = None,pars = None,Vz = None,rho0z = None,state_z = None,timevary_stiff_flag = None,flength_id = None,DDW = None): 
    
    dofg = Kgg.shape[1-1]
    
    miud = 0.05
    miudx = 0.05
    nodesum = dofg / 5
    tspan = np.transpose((np.arange(0,time+dt,dt)))
    
    ndt = np.asarray(tspan).size
    
    #初始化响应
    Ug = np.zeros((dofg,ndt))
    Vg = np.zeros((dofg,ndt))
    Ag = np.zeros((dofg,ndt))
    uxg = np.zeros((dofg / 5,ndt))
    uyg = np.zeros((dofg / 5,ndt))
    
    uxg1 = np.zeros((dofg / 5,ndt))
    uyg1 = np.zeros((dofg / 5,ndt))
    uzg = np.zeros((dofg / 5,ndt))
    Nx = np.zeros((dofg / 5 - 1,ndt))
    contact_force.Fx_local = np.zeros((dofg / 5,ndt))
    contact_force.Fy_local = np.zeros((dofg / 5,ndt))
    contact_force.Fn_local = np.zeros((dofg / 5,ndt))
    Fv1 = np.zeros((dofg / 5,ndt))
    #初始化newmark算法参数
    gama = 0.5
    delta = 0.25
    
    a0 = 1 / delta / dt / dt
    a1 = gama / delta / dt
    a2 = 1 / delta / dt
    a3 = 1 / 2 / delta - 1
    a4 = gama / delta - 1
    a5 = dt / 2 * (gama / delta - 2)
    a6 = dt * (1 - gama)
    a7 = gama * dt
    #施加约束
    gset = np.arange(1,dofg+1,1)
    cset = (np.arange(1,25+1))
    
    for i in np.arange(1,len(flength_id)+1).reshape(-1):
        nns1[:,i] = np.arange((flength_id(i) * 5 - 20),(flength_id(i) * 5 + 20)+1)
    
    B12 = np.transpose((__builtint__.sorted(nns1)))
    cset = np.array([cset,B12])
    
    #      cset=[1:5];##
    aset = gset
    aset[cset] = []
    Kaa = Kgg(aset,aset)
    Maa = Mgg(aset,aset)
    Caa = Cgg(aset,aset)
    #计算初始加速度
    Fg,uxg[:,1],uyg[:,1],uzg[:,1],Nx[:,1],contact_force.Fx_local[:,1],contact_force.Fy_local[:,1],contact_force.Fn_local[:,1],Fv1[:,1] = compute_load_vec(dofg,nodes,pars,Ug(:,1),Vg(:,1),transmat,Vz,rho0z,state_z,DDW)
    #     Fhit=create_hit_load(Ug(:,1),Vg(:,1),pars.khit,pars.khit,pars.chit,miud,miudx,pars.Rvo,DDW,pars.mesh,transmat);
    Ag[aset,1] = np.linalg.solve(Maa,(Fgravg(aset) + Fg(aset) - Kaa * Ug(aset,1) - Caa * Vg(aset,1)))
    
    Keq = Kaa + a0 * Maa + a1 * Caa
    if timevary_stiff_flag == 0:
        Seq = np.linalg.solve(Keq,np.eye(np.asarray(aset).size))
    
    #迭代计算
    for i in np.arange(2,ndt+1).reshape(-1):
        #计算等效载荷以及返回单元坐标系下节点的位移响应
        Fg,uxg[:,i],uyg[:,i],uzg[:,i],Nx[:,i],contact_force.Fx_local[:,i],contact_force.Fy_local[:,i],contact_force.Fn_local[:,i],Fv1[:,i] = compute_load_vec(dofg,nodes,pars,Ug(:,i - 1),Vg(:,i - 1),transmat,Vz,rho0z,state_z,DDW)
        #加碰撞载荷
#       for j=1:length(uxg(:,1))
#         omega1(j)=sqrt(uxg(j,i)^2+uyg(j,i)^2);
#         vr(j)=sqrt(Vg(j*5-3,i-1)^2+Vg(j*5-1,i-1)^2); #有问题
#         deta1s(j)=Rt(j)-rt(j);
#         if  omega1(j)>deta1s(j)
#         deta111(j)=omega1(j)-deta1s(j);
#         FhitN(j)=-(deta111(j)-(Rt(j)-rt(j)))*pars.khit-vr(j)*pars.chit;
#         Fhitf(j)=FhitN(j)*0.243;
#          #计算接触力
#          #计算摩擦力
#         else
#         end
#       end
#        Fhit=create_hit_load(Ug(:,i-1),Vg(:,i-1),pars.khit,pars.khit,pars.chit,miud,miudx,pars.Rvo,DDW,pars.mesh,transmat);
        Feq = Fgravg(aset) + Fg(aset) + Maa * (a0 * Ug(aset,i - 1) + a2 * Vg(aset,i - 1) + a3 * Ag(aset,i - 1)) + + Caa * (a1 * Ug(aset,i - 1) + a4 * Vg(aset,i - 1) + a5 * Ag(aset,i - 1))
        #是否考虑更新时变刚度
        if timevary_stiff_flag == 1:
            Kggadd = create_timevary_stiff(Ug(:,i - 1),transmat,nodes,pars)
            Keq_time = Keq + Kggadd(aset,aset)
            Ug[aset,i] = np.linalg.solve(Keq_time,Feq)
        else:
            Ug[aset,i] = Seq * Feq
        #更新速度加速度
        Ag[aset,i] = a0 * (Ug(aset,i) - Ug(aset,i - 1)) - a2 * Vg(aset,i - 1) - a3 * Ag(aset,i - 1)
        Vg[aset,i] = Vg(aset,i - 1) + a6 * Ag(aset,i - 1) + a7 * Ag(aset,i)
        for k in np.arange(2,nodesum+1).reshape(-1):
            uxg1[k,i] = Ug(5 * k - 3,i)
            uyg1[k,i] = Ug(5 * k - 1,i)
    
    uxg1 = uxg1 / 100
    return Ug,Vg,Ag,uxg1,uyg1,uzg,Nx,contact_force,tspan,Fv1
    
    return Ug,Vg,Ag,uxg1,uyg1,uzg,Nx,contact_force,tspan,Fv1