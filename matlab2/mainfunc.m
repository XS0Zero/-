function mainfunc()
tic
clear;
clc;
dt=0.001;
time=60;        %����ʱ�䲽���ͼ���ʱ��
wellbore_state_dz=1;           %���㾮����״̬���״̬���������ȵĲ���ȡֵ
timevary_stiff_flag=0;         %�Ƿ���ʱ��նȾ��󣬿�����Ϊ
%---------------------�������----------------------% a
drcs=csvread('��������2.csv');
Drcs=csvread('��������.csv');
id_im=length(drcs(:,1));
id_im1=length(Drcs(:,1));
drcs1=cell(id_im,1); 
for i=1:id_im  
last_nonzero_index = find(drcs(i,:)~=0, 1, 'last');
drcs11=drcs(i,1:last_nonzero_index);
drcs1{i}=drcs11;
end
for i=1:id_im1  
last_nonzero_index = find(Drcs(i,:)~=0, 1, 'last');
Drcs11=Drcs(i,1:last_nonzero_index);
Drcs1{i}=Drcs11;
end
%���Ϊ�գ�������Ϊ0
mms=length(drcs1);
for i=1:mms
    if isempty(drcs1{i})==1
        drcs1{i}=0;
    end
end  
fgqwz=drcs1{12};%������λ��
flength_id=Drcs1{8}*2;
% data1=zeros(1,3);
if length(drcs1{9})~=length(drcs1{10})||length(drcs1{9})~=length(drcs1{11})
    drcs1{10}=drcs(10,1:length(drcs1{9}));
    drcs1{11}=drcs(11,1:length(drcs1{9}));
end
data=[drcs1{9};drcs1{10};drcs1{11}]';
data(end,1)=round(data(end,1));
% data=[data1;data];
%---------------------����Ĭ�ϲ���----------------------%

pars=get_model_param(drcs1,data,Drcs1);                 %����������

[Ss,Xs,Ys,Zs,alphas,phis]=deal_input_data(data);
% pars.DT=(pars.Tint-pars.Tint1)/Zs(end);

C=[pars.Rvi*2;pars.Rvo*2;pars.Ls]';
B=[pars.DW;pars.LLS]';  
[Rt1,rt1,It1]=banjing(C);
[DDW]=banjing1(B); 
for i=1:sum(pars.mesh)+1
    if i==1
        DDDW(1)=DDW(1);
    else
        mmsn(i)=20*i;
        if mmsn(i)>=length(DDW)
           DDDW(i)=DDW(end);
        else
           DDDW(i)=DDW(mmsn(i)); 
        end
    end
end
DDDW= DDDW';
%��ⲻͬ��ȵ������ٶȺ��ܶȣ�����ת���ɴӾ��ڵ����ף�״̬�洹��仯
[Vz,pz,Tz,rho0z,state_z,Tei]=cal_wellbore_state(pars,wellbore_state_dz,Ss,Zs,alphas,rt1);

%���ϵͳ�ĸն������������
%ע������Ԫģ�͵�Ԫ����ϵX,YΪ����ZΪ���򣬵�Ԫ����ϵ�½ڵ����ɶ�˳��Ϊ��z,x,ry,y,rx
[Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2]=create_model(Vz,rho0z,state_z,pars,Ss,Xs,Ys,Zs,alphas,phis);
%����ϵͳ����Ӧ
%����ϵͳ��ȫ������ϵ��ÿ���ڵ��������ɶ���ӦUg,Vg,Ag����Ԫ����ϵ�½ڵ������ƽ����Ӧux,uy,uz��ʱ������

                        %�׹ܰ뾶�ؾ���ֲ�
[Ug,Vg,Ag,ux,uy,uz,Nx,contact_force,tspan,Fv1]=newmark_compute(dt,time,Mgg,Kgg,Cgg,Fgravg,transmat,nodes,pars,Vz,rho0z,state_z,timevary_stiff_flag,flength_id,DDDW);
for i=1:length(ux(:,1))
    uuxx(i)=(ux(i,5000));
end
ss22=length(ux(:,1));
ddep=0:(pars.LS/(ss22-1)):pars.LS;
UXX=[ddep;uuxx]';
csvwrite('��λ����ܳ��仯.csv',UXX);
end
