function [Vz,pzz,TTT1,rho0z,state_z,Tei]=cal_wellbore_state(pars,wellbore_state_dz,Ss,Zs,alphas,rt1)
    Y0=[pars.Vint;pars.pint;pars.Tint;pars.rhoint];         %���׳�ʼ����
    %�Ӿ����򾮿ڼ���
    maxz=sum(pars.Ls)-1;
    [zs,Ys,Tei]=ode45(@(z,Y)odefunc(z,Y,pars,maxz,Zs,alphas,Ss),0:wellbore_state_dz:maxz,Y0);
    %������ת��Ϊ�Ӿ��ڵ�����
    Ys=Ys(end:-1:1,:);
    state_z=zs;
%     Vz=Ys(:,1);
    pz=Ys(:,2);
    Tz=Ys(:,3);
%     rho0z11=(Ys(:,4));
%     ss1=(rho0z11*0.01*pars.Q/10000);
%     rho0z1=ss1+(rho0z11(end)-ss1(end));
%     rho0z= rho0z1*(-1)+2*pars.rhoint;
    %�����ͼ
    rho0z=zeros(length(Tz),1);
    Vz=zeros(length(Tz),1);
    for i=1:length(Tz)
     rho0z(i)=3484.4*(pars.gama/pars.Zg)*(pz(i)/1000000/(Tz(i)+273.15));
%      Vz(i)=(pars.Zg*pars.wi)/(86400*rho0z(i)*pi*rt1(i)^2);
     Vz(i)=5e-9*(pars.Q*pars.Zg*(Tz(i)+273))/((rt1(i)*2)^2*pz(i)/10^(6));
    end
[pzz,TTT]=czyl(pars,Vz,rho0z,Tz,Ss,Zs,alphas);
TTT1=TTT';
end

%
function [dYdz,Tei]=odefunc(z,Y,pars,maxz,Zs,alphas,Ss)
    %΢�ַ��̳�ʼ����Ϊ���ף���˽�΢�ַ���ת��Ϊ�Ӿ��׵����ڵ�΢�֣���dz��Ϊ-dz
    g=9.81;
    %��ȡ��ǰ���״̬
    V=Y(1);
    p=Y(2);
    T=Y(3);
    rho0=Y(4);
    %����һЩ����
    zup=maxz-z;         %��ǰλ�þ��뾮�ھ���
    zup1=interp1(Ss,Zs,zup);           %��ǰλ�ô���
    Tei=pars.Tint1+pars.DT*zup1;            %�ز��¶�
    Re=rho0*V*2*pars.RRO(1)/pars.miu;      %��ŵ��
%     f=1/(-2*log(pars.im/2/pars.Rvi(1)/3.715+(6.943/Re)^0.9))^2;
    f=1/((4*log(pars.im/(2*3.715*pars.RRO(1))+(6.943/Re)^0.9)^2));
    dpdzfr=f*rho0*V^2/2/pars.RRO(1);
    %���㵱ǰλ�þ�б��
   
    alpha=interp1(Ss,alphas,zup);           %��ǰλ�þ�б��  
    %����ѹ������Zg
%     pr=p/pars.PC;
%     tr=(T+273)/pars.TC;
%     if 8<=pr&&pr<15&&tr>1.05&&tr<3.0
%         X1=-0.002225*tr^4+0.0108* tr^3+0.015225* tr^2-0.153225*tr+0.241575;
%         X2=0.1045*tr^4-0.8602*tr^3+2.3695* tr^2-2.1065*tr+0.6299;
%     else
%         X1=0.0148*tr^4+0.13881666* tr^3+0.49025* tr^2-0.79468333*tr+0.55123333;
%         X2=0.4505*tr^4-4.2282333*tr^3+14.9684* tr^2-24.3115666*tr+17.9842667;
%     end
%     
% %     ZZg=X1*pr+X2;
%     ZZg=1.59-(5700-zup)*0.0001035;
    %΢�ַ���:ԭ΢�ַ���Ϊ����΢�֣������Ϊ�˷���΢�֣��Ӿ����򾮿ڼ���dp/dz--->dp/(-dz),���ʽ����Ӧ����
    %drho0/dz
    drho0=-((T*rho0*g*cos(alpha)+T*dpdzfr-rho0*g*cos(alpha)/pars.cp-...
        p/pars.cp*(2*pi*pars.Rmax*pars.ke*pars.Ua*(T-Tei))/(pars.wi*(pars.ke+pars.Rmax*pars.Ua*pars.ft)))/...
        (pars.Zg*pars.Rg*T^2/pars.M-T*V^2+p*V^2/pars.cp/rho0));
    %dV/dz
%     dV=-(V/rho0*(drho0));
    dV=(V*(drho0)/rho0);
    %dp/dz
    dp=-(rho0*g*cos(alpha)+dpdzfr-rho0*V*(dV));
    %dT/dz
    dT=-((g*cos(alpha)-V*(dV)+...
        2*pi*pars.Rmax*pars.ke*pars.Ua*(T-Tei)/(pars.wi*(pars.ke+pars.Rmax*pars.Ua*pars.ft)))/pars.cp);
    %����
    
    dYdz=[dV;dp;dT;drho0];
end