function [Fg,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt,Fv1]=compute_load_vec(dofg,nodes,pars,Ugt,Vgt,transmat,Vz,rho0z,state_z,DDW1)
    %��������������������������ͱ���Ӵ���
    
    %��������������
   [Fv,Fv1]=create_flow_force(dofg,nodes,Ugt,pars,transmat,Vz,rho0z,state_z);
    
    %����Ӵ���
    [Fcontact,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt]=create_contact_force(dofg,nodes,Ugt,Vgt,pars,transmat,DDW1);
    
    %�ۺ�
    Fg=Fv+Fcontact;
end

function [Fv,Fv1]=create_flow_force(dofg,nodes,Ugt,pars,transmat,Vz,rho0z,state_z)
    Fv=zeros(dofg,1);
    nelem=sum(pars.mesh);
    Fv1=zeros(dofg/5,1);
    %��ֵ����
    phix=@(z,le)[0;
               1-3*z^2/le^2+2*z^3/le^3;
               z-2*z^2/le+z^3/le^2;
               0;
               0;
               0;
               3*z^2/le^2-2*z^3/le^3;
               -z^2/le+z^3/le^2;
               0;...
               0];
       phiy=@(z,le)[0;
             0;
             0;
             1-3*z^2/le^2+2*z^3/le^3;
             -(z-2*z^2/le+z^3/le^2);
             0;
             0;
             0;
             3*z^2/le^2-2*z^3/le^3;
             -(-z^2/le+z^3/le^2)];
    for i=1:nelem
        Ue=Ugt(i*5-4:i*5+5);
        ue=transmat{i}*Ue;             %��Ԫ����ϵ�µ�Ԫλ������
        z1=nodes(i,3);
        z2=nodes(i+1,3);            %��Ԫ�����ڵ�Ĵ���
        %��Ԫ����
        le=nodes(i+1,4)-nodes(i,4);
        %���㵥Ԫ�в����ڴ���������ܶȺ�����
        zzs=round((z1+z2)/2);
        rho0=rho0z(zzs);
        V=Vz(zzs); 
%         rho0=interp1(state_z,rho0z,(z1+z2)/2,'spline');
%         V=interp1(state_z,Vz,(z1+z2)/2,'spline');
        %��Ԫ������������ڵ�ƽ��
        A0=((pi*nodes(i,8)^2-pi*nodes(i,7)^2)+(pi*nodes(i+1,8)^2-pi*nodes(i+1,7)^2))/2;
        %��Ԫ�����ڵ�λ�õľ�б�Ƿ�λ�ǣ����Ǳ��θ���
        alpha1=nodes(i,5)+ue(3);
        alpha2=nodes(i+1,5)+ue(8);
        phi1=nodes(i,6)+ue(5);
        phi2=nodes(i+1,6)+ue(10);
        if abs(phi1-phi2)<=pi
            detphi=(phi2-phi1);
        elseif  phi1>phi2
            detphi=-abs((2*pi-phi1)+phi2);
        elseif  phi2>phi1
            detphi=abs((2*pi-phi2)+phi1);
        end
        Fx=-rho0*A0*V^2*sin(alpha2-alpha1)*cos(detphi);
        Fy=-rho0*A0*V^2*sin(alpha2-alpha1)*sin(detphi);
        Fz=-rho0*A0*V^2*cos(alpha2-alpha1);
%         Fx=0;
%         Fy=0;
%         Fz=0;
        %�غ���Ϊ�����غ������ڵ�Ԫ�в��������䵥Ԫ����ϵ�µ�Ч�ڵ���
        phiz=@(z,le)[1-z/le;0;0;0;0;z/le;0;0;0;0];
        fe=phix(le/2,le)*Fx+phiy(le/2,le)*Fy+phiz(le/2,le)*Fz;
%         Fe=transmat{i}'*fe;          %�任��ȫ������ϵ
        Fv(i*5-4:i*5+5)=Fv(i*5-4:i*5+5)+fe;          %��װ�غ�����
        Fv1(i)=Fv((i-1)*5+6);
    end
end


function [Fcontact,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt]=create_contact_force(dofg,nodes,Ugt,Vgt,pars,transmat,DDW1)
    Fcontact=zeros(dofg,1);
    uxgt=zeros(dofg/5,1);
    uygt=zeros(dofg/5,1);
    uzgt=zeros(dofg/5,1);
    Nxt=zeros(dofg/5-1,1);
    Fxt=zeros(dofg/5,1);
    Fyt=zeros(dofg/5,1);
    Fnt=zeros(dofg/5,1);
    for i=2:size(nodes,1)         %���˹�֧�������ǽӴ���
        %���㵥Ԫ����ϵ�½ڵ��λ�ƺ��ٶ�
        Ue=Ugt((i-2)*5+1:(i-1)*5+5);
        ue=transmat{i-1}*Ue;
        %��ȡ�ڵ���������λ��
        uxgt(i)=ue(7);
        uygt(i)=ue(9);
        uzgt(i)=ue(6);
        ux=ue(7);
        uy=ue(9);
        Ve=Vgt((i-2)*5+1:(i-1)*5+5);
        ve=transmat{i-1}*Ve;
        vx=ve(7);
        vy=ve(9);
        %
        %����Ӵ�����
        R1=(nodes(i,8));
        R2=DDW1(i);
        delta=sqrt(ux^2+uy^2)-(R2-R1);
        if delta>0    %�����Ӵ�
            %����Ӵ��ٶ�
            vvec=[vx;vy];
            uvec=[ux;uy];
            vn=vvec'*uvec/norm(uvec,2);         %����Ӵ��ٶȴ�С
            vnvec=vn*uvec/norm(uvec,2);         %����Ӵ��ٶ�ʸ��
            vtvec=vvec-vnvec;                   %����Ӵ��ٶ�ʸ��
            %���㷨��Ӵ���������Ħ����
            Fn=pars.khit*delta^1.5+pars.chit*vn*(vn>0);
            Ft=Fn*pars.ksi;
            %�غ���x,y����ͶӰ
            Fxy=-[Fn*uvec(1)/norm(uvec,2);Fn*uvec(2)/norm(uvec,2)]-[Ft*vtvec(1)/norm(vtvec,2);Ft*vtvec(2)/norm(vtvec,2)];
            %��Ԫ����ϵ���غ�
%             fe=[0;0;0;0;0;Ft;Fxy(1);0;Fxy(2);0];
            fe=[0;0;0;0;0;0;Fxy(1);0;Fxy(2);0];
            Fcontact((i-2)*5+1:(i-1)*5+5)=Fcontact((i-2)*5+1:(i-1)*5+5)+transmat{i-1}'*fe;
            %��ȡ�Ӵ���
            Fxt(i)=Fxy(1);
            Fyt(i)=Fxy(2);
            Fnt(i)=Fn;      %����Ӵ�����������������
            %plot_state(R2-R1,ux,uy,45,i);
        end
        %���㵥Ԫ������
        A1=pi*nodes(i-1,8)^2-pi*nodes(i-1,7)^2;
        A2=pi*nodes(i,8)^2-pi*nodes(i,7)^2;         %��Ԫ�����ڵ��Ӧ�������
        le=norm(nodes(i,1:3)-nodes(i-1,1:3),2);
        Nxt(i-1)=(ue(6)-ue(1))*pars.Ev*(A1+A2)/2/le;
    end
    
end


function plot_state(R,ux,uy,select_node,nowpoint)
    if nowpoint~=select_node
        return
    end
    theta=0:0.01:2*pi;
    figure(100)
    plot(R*cos(theta),R*sin(theta),'r')
    hold on
    scatter(ux,uy)
    hold off
    pause(0.0001)
end