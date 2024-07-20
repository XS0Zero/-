function [Fg,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt,Fv1]=compute_load_vec(dofg,nodes,pars,Ugt,Vgt,transmat,Vz,rho0z,state_z,DDW1)
    %计算管柱的受力，包括流体力和壁面接触力
    
    %计算流体作用力
   [Fv,Fv1]=create_flow_force(dofg,nodes,Ugt,pars,transmat,Vz,rho0z,state_z);
    
    %计算接触力
    [Fcontact,uxgt,uygt,uzgt,Nxt,Fxt,Fyt,Fnt]=create_contact_force(dofg,nodes,Ugt,Vgt,pars,transmat,DDW1);
    
    %综合
    Fg=Fv+Fcontact;
end

function [Fv,Fv1]=create_flow_force(dofg,nodes,Ugt,pars,transmat,Vz,rho0z,state_z)
    Fv=zeros(dofg,1);
    nelem=sum(pars.mesh);
    Fv1=zeros(dofg/5,1);
    %插值函数
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
        ue=transmat{i}*Ue;             %单元坐标系下单元位移向量
        z1=nodes(i,3);
        z2=nodes(i+1,3);            %单元两个节点的垂深
        %单元长度
        le=nodes(i+1,4)-nodes(i,4);
        %计算单元中部所在垂深的流体密度和流速
        zzs=round((z1+z2)/2);
        rho0=rho0z(zzs);
        V=Vz(zzs); 
%         rho0=interp1(state_z,rho0z,(z1+z2)/2,'spline');
%         V=interp1(state_z,Vz,(z1+z2)/2,'spline');
        %单元截面积，两个节点平均
        A0=((pi*nodes(i,8)^2-pi*nodes(i,7)^2)+(pi*nodes(i+1,8)^2-pi*nodes(i+1,7)^2))/2;
        %单元两个节点位置的井斜角方位角，考虑变形附加
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
        %载荷作为集中载荷作用在单元中部，计算其单元坐标系下等效节点力
        phiz=@(z,le)[1-z/le;0;0;0;0;z/le;0;0;0;0];
        fe=phix(le/2,le)*Fx+phiy(le/2,le)*Fy+phiz(le/2,le)*Fz;
%         Fe=transmat{i}'*fe;          %变换到全局坐标系
        Fv(i*5-4:i*5+5)=Fv(i*5-4:i*5+5)+fe;          %组装载荷向量
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
    for i=2:size(nodes,1)         %两端固支，不考虑接触力
        %计算单元坐标系下节点的位移和速度
        Ue=Ugt((i-2)*5+1:(i-1)*5+5);
        ue=transmat{i-1}*Ue;
        %提取节点三个方向位移
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
        %计算接触变形
        R1=(nodes(i,8));
        R2=DDW1(i);
        delta=sqrt(ux^2+uy^2)-(R2-R1);
        if delta>0    %发生接触
            %法向接触速度
            vvec=[vx;vy];
            uvec=[ux;uy];
            vn=vvec'*uvec/norm(uvec,2);         %法向接触速度大小
            vnvec=vn*uvec/norm(uvec,2);         %法向接触速度矢量
            vtvec=vvec-vnvec;                   %切向接触速度矢量
            %计算法向接触力和切向摩擦力
            Fn=pars.khit*delta^1.5+pars.chit*vn*(vn>0);
            Ft=Fn*pars.ksi;
            %载荷在x,y方向投影
            Fxy=-[Fn*uvec(1)/norm(uvec,2);Fn*uvec(2)/norm(uvec,2)]-[Ft*vtvec(1)/norm(vtvec,2);Ft*vtvec(2)/norm(vtvec,2)];
            %单元坐标系下载荷
%             fe=[0;0;0;0;0;Ft;Fxy(1);0;Fxy(2);0];
            fe=[0;0;0;0;0;0;Fxy(1);0;Fxy(2);0];
            Fcontact((i-2)*5+1:(i-1)*5+5)=Fcontact((i-2)*5+1:(i-1)*5+5)+transmat{i-1}'*fe;
            %提取接触力
            Fxt(i)=Fxy(1);
            Fyt(i)=Fxy(2);
            Fnt(i)=Fn;      %法向接触力，不包括切向力
            %plot_state(R2-R1,ux,uy,45,i);
        end
        %计算单元轴向力
        A1=pi*nodes(i-1,8)^2-pi*nodes(i-1,7)^2;
        A2=pi*nodes(i,8)^2-pi*nodes(i,7)^2;         %单元两个节点对应截面面积
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