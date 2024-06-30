import numpy as np

dt = 0.001
time = 60

wellbore_state_dz = 1

timevary_stiff_flag = 0

#---------------------�������----------------------# a
drcs = csvread('��������2.csv')
Drcs = csvread('��������.csv')
id_im = len(drcs(:,1))
id_im1 = len(Drcs(:,1))
drcs1 = cell(id_im,1)
for i in np.arange(1,id_im+1).reshape(-1):
    last_nonzero_index = find(drcs(i,:) != 0,1,'last')
    drcs11 = drcs(i,np.arange(1,last_nonzero_index+1))
    drcs1[i] = drcs11

for i in np.arange(1,id_im1+1).reshape(-1):
    last_nonzero_index = find(Drcs(i,:) != 0,1,'last')
    Drcs11 = Drcs(i,np.arange(1,last_nonzero_index+1))
    Drcs1[i] = Drcs11

#���Ϊ�գ�������Ϊ0
mms = len(drcs1)
for i in np.arange(1,mms+1).reshape(-1):
    if len(drcs1[i])==0 == 1:
        drcs1[i] = 0

fgqwz = drcs1[12]

flength_id = Drcs1[8] * 2
# data1=zeros(1,3);
if len(drcs1[9]) != len(drcs1[10]) or len(drcs1[9]) != len(drcs1[11]):
    drcs1[10] = drcs(10,np.arange(1,len(drcs1[9])+1))
    drcs1[11] = drcs(11,np.arange(1,len(drcs1[9])+1))

data = np.transpose(np.array([[drcs1[9]],[drcs1[10]],[drcs1[11]]]))
data[end(),1] = np.round(data(end(),1))
# data=[data1;data];
#---------------------����Ĭ�ϲ���----------------------#

pars = get_model_param(drcs1,data,Drcs1)

Ss,Xs,Ys,Zs,alphas,phis = deal_input_data(data)
# pars.DT=(pars.Tint-pars.Tint1)/Zs(end);

C = np.transpose(np.array([[pars.Rvi * 2],[pars.Rvo * 2],[pars.Ls]]))
B = np.transpose(np.array([[pars.DW],[pars.LLS]]))
Rt1,rt1,It1 = banjing(C)
DDW = banjing1(B)
for i in np.arange(1,sum(pars.mesh) + 1+1).reshape(-1):
    if i == 1:
        DDDW[1] = DDW(1)
    else:
        mmsn[i] = 20 * i
        if mmsn(i) >= len(DDW):
            DDDW[i] = DDW(end())
        else:
            DDDW[i] = DDW(mmsn(i))

DDDW = np.transpose(DDDW)
#��ⲻͬ��ȵ������ٶȺ��ܶȣ�����ת���ɴӾ��ڵ����ף�״̬�洹��仯
Vz,pz,Tz,rho0z,state_z,Tei = cal_wellbore_state(pars,wellbore_state_dz,Ss,Zs,alphas,rt1)
#���ϵͳ�ĸն������������
#ע������Ԫģ�͵�Ԫ����ϵX,YΪ����ZΪ���򣬵�Ԫ����ϵ�½ڵ����ɶ�˳��Ϊ��z,x,ry,y,rx
Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2 = create_model(Vz,rho0z,state_z,pars,Ss,Xs,Ys,Zs,alphas,phis)
#����ϵͳ����Ӧ
#����ϵͳ��ȫ������ϵ��ÿ���ڵ��������ɶ���ӦUg,Vg,Ag����Ԫ����ϵ�½ڵ������ƽ����Ӧux,uy,uz��ʱ������

#�׹ܰ뾶�ؾ���ֲ�
Ug,Vg,Ag,ux,uy,uz,Nx,contact_force,tspan,Fv1 = newmark_compute(dt,time,Mgg,Kgg,Cgg,Fgravg,transmat,nodes,pars,Vz,rho0z,state_z,timevary_stiff_flag,flength_id,DDDW)
for i in np.arange(np.arange(1,len(ux(,,1))+1)):
    uuxx[i] = (ux(i,5000))

ss22 = len(ux(:,1))
ddep = np.arange(0,pars.LS+(pars.LS / (ss22 - 1)),(pars.LS / (ss22 - 1)))
UXX = np.transpose(np.array([[ddep],[uuxx]]))
csvwrite('��λ����ܳ��仯.csv',UXX)