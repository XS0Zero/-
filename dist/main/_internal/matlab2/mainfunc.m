function mainfunc()
tic
clear;
clc;
dt=0.001;
time=60;        %计算时间步长和计算时间
wellbore_state_dz=1;           %计算井流体状态输出状态结果关于深度的步长取值
timevary_stiff_flag=0;         %是否考虑时变刚度矩阵，考虑则为
%---------------------导入参数----------------------% a
drcs=csvread('输入数据2.csv');
Drcs=csvread('输入数据.csv');
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
%如果为空，则令其为0
mms=length(drcs1);
for i=1:mms
    if isempty(drcs1{i})==1
        drcs1{i}=0;
    end
end  
fgqwz=drcs1{12};%多封隔器位置
flength_id=Drcs1{8}*2;
% data1=zeros(1,3);
if length(drcs1{9})~=length(drcs1{10})||length(drcs1{9})~=length(drcs1{11})
    drcs1{10}=drcs(10,1:length(drcs1{9}));
    drcs1{11}=drcs(11,1:length(drcs1{9}));
end
data=[drcs1{9};drcs1{10};drcs1{11}]';
data(end,1)=round(data(end,1));
% data=[data1;data];
%---------------------设置默认参数----------------------%

pars=get_model_param(drcs1,data,Drcs1);                 %定义计算参数

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
%求解不同深度的流体速度和密度，数据转换成从井口到井底，状态随垂深变化
[Vz,pz,Tz,rho0z,state_z,Tei]=cal_wellbore_state(pars,wellbore_state_dz,Ss,Zs,alphas,rt1);

%求解系统的刚度质量阻尼矩阵
%注意有限元模型单元坐标系X,Y为横向Z为轴向，单元坐标系下节点自由度顺序为：z,x,ry,y,rx
[Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2]=create_model(Vz,rho0z,state_z,pars,Ss,Xs,Ys,Zs,alphas,phis);
%计算系统动响应
%返回系统在全局坐标系下每个节点的五个自由度响应Ug,Vg,Ag，单元坐标系下节点的三个平动响应ux,uy,uz和时间序列

                        %套管半径沿井深分布
[Ug,Vg,Ag,ux,uy,uz,Nx,contact_force,tspan,Fv1]=newmark_compute(dt,time,Mgg,Kgg,Cgg,Fgravg,transmat,nodes,pars,Vz,rho0z,state_z,timevary_stiff_flag,flength_id,DDDW);
for i=1:length(ux(:,1))
    uuxx(i)=(ux(i,5000));
end
ss22=length(ux(:,1));
ddep=0:(pars.LS/(ss22-1)):pars.LS;
UXX=[ddep;uuxx]';
csvwrite('振动位移随管长变化.csv',UXX);
end
