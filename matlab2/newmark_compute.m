function [Ug,Vg,Ag,uxg1,uyg1,uzg,Nx,contact_force,tspan,Fv1]=newmark_compute(dt,time,Mgg,Kgg,Cgg,Fgravg,transmat,nodes,pars,Vz,rho0z,state_z,timevary_stiff_flag,flength_id,DDW)
    %
    dofg=size(Kgg,1);           %�������ɶ���Ŀ
    miud=0.05;
    miudx=0.05;
    nodesum=dofg/5;
    tspan=(0:dt:time)';         %ʱ������
    ndt=numel(tspan);           %
    %��ʼ����Ӧ
    Ug=zeros(dofg,ndt);
    Vg=zeros(dofg,ndt);
    Ag=zeros(dofg,ndt);
    uxg=zeros(dofg/5,ndt);
    uyg=zeros(dofg/5,ndt);       %�洢��Ԫ����ϵ�¸����ڵ�ĺ���λ�ƺ�����λ��
    uxg1=zeros(dofg/5,ndt);
    uyg1=zeros(dofg/5,ndt); 
    uzg=zeros(dofg/5,ndt);
    Nx=zeros(dofg/5-1,ndt);
    contact_force.Fx_local=zeros(dofg/5,ndt);
    contact_force.Fy_local=zeros(dofg/5,ndt);
    contact_force.Fn_local=zeros(dofg/5,ndt);
    Fv1=zeros(dofg/5,ndt);
    %��ʼ��newmark�㷨����
    gama=0.5;
    delta=0.25;         %newmark-beta�㷨����
    a0=1/delta/dt/dt;
    a1=gama/delta/dt;
    a2=1/delta/dt;
    a3=1/2/delta-1;
    a4=gama/delta-1;
    a5=dt/2*(gama/delta-2);
    a6=dt*(1-gama);
    a7=gama*dt;
    %ʩ��Լ��
    gset=1:1:dofg;
    cset=(1:25);%%
    for i=1:length(flength_id)
        nns1(:,i)=(flength_id(i)*5-20):(flength_id(i)*5+20);
    end
    B12=(sort(nns1(:)))';
    cset=[cset,B12];%%
%      cset=[1:5];%%
    aset=gset;
    aset(cset)=[];
    Kaa=Kgg(aset,aset);
    Maa=Mgg(aset,aset);
    Caa=Cgg(aset,aset);
    %�����ʼ���ٶ�
    [Fg,uxg(:,1),uyg(:,1),uzg(:,1),Nx(:,1),contact_force.Fx_local(:,1),...
        contact_force.Fy_local(:,1),contact_force.Fn_local(:,1),Fv1(:,1)]=...
        compute_load_vec(dofg,nodes,pars,Ug(:,1),Vg(:,1),transmat,Vz,rho0z,state_z,DDW);
%     Fhit=create_hit_load(Ug(:,1),Vg(:,1),pars.khit,pars.khit,pars.chit,miud,miudx,pars.Rvo,DDW,pars.mesh,transmat);
    Ag(aset,1)=Maa\(Fgravg(aset)+Fg(aset)-Kaa*Ug(aset,1)-Caa*Vg(aset,1));%
    Keq=Kaa+a0*Maa+a1*Caa;
    if timevary_stiff_flag==0
         Seq=Keq\eye(numel(aset));%����û��������ɶЧ��
    end
    %��������
    for i=2:ndt

        %�����Ч�غ��Լ����ص�Ԫ����ϵ�½ڵ��λ����Ӧ
        [Fg,uxg(:,i),uyg(:,i),uzg(:,i),Nx(:,i),contact_force.Fx_local(:,i),...
        contact_force.Fy_local(:,i),contact_force.Fn_local(:,i),Fv1(:,i)]=...
        compute_load_vec(dofg,nodes,pars,Ug(:,i-1),Vg(:,i-1),transmat,Vz,rho0z,state_z,DDW);
       %����ײ�غ�
%       for j=1:length(uxg(:,1))
%         omega1(j)=sqrt(uxg(j,i)^2+uyg(j,i)^2);
%         vr(j)=sqrt(Vg(j*5-3,i-1)^2+Vg(j*5-1,i-1)^2); %������
%         deta1s(j)=Rt(j)-rt(j);
%         if  omega1(j)>deta1s(j)
%         deta111(j)=omega1(j)-deta1s(j);
%         FhitN(j)=-(deta111(j)-(Rt(j)-rt(j)))*pars.khit-vr(j)*pars.chit;
%         Fhitf(j)=FhitN(j)*0.243;
%          %����Ӵ���
%          %����Ħ����
%         else
%         end
%       end
%        Fhit=create_hit_load(Ug(:,i-1),Vg(:,i-1),pars.khit,pars.khit,pars.chit,miud,miudx,pars.Rvo,DDW,pars.mesh,transmat);
       Feq=Fgravg(aset)+Fg(aset)+Maa*(a0*Ug(aset,i-1)+a2*Vg(aset,i-1)+a3*Ag(aset,i-1))+...
       +Caa*(a1*Ug(aset,i-1)+a4*Vg(aset,i-1)+a5*Ag(aset,i-1));     %������ײ�غ�
        %�Ƿ��Ǹ���ʱ��ն�
        if timevary_stiff_flag==1
            Kggadd=create_timevary_stiff(Ug(:,i-1),transmat,nodes,pars);
            Keq_time=Keq+Kggadd(aset,aset);
            Ug(aset,i)=Keq_time\Feq;            %����λ��
        else
            Ug(aset,i)=Seq*Feq;                 %����λ��
        end

        

        %�����ٶȼ��ٶ�
        Ag(aset,i)=a0*(Ug(aset,i)-Ug(aset,i-1))-a2*Vg(aset,i-1)-a3*Ag(aset,i-1);
        Vg(aset,i)=Vg(aset,i-1)+a6*Ag(aset,i-1)+a7*Ag(aset,i);
for k=2:nodesum   
        uxg1(k,i)=Ug(5*k-3,i);
        uyg1(k,i)=Ug(5*k-1,i);   
end        
    end
 
 uxg1=uxg1/100;   
    
end

