function [Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2]=create_model(Vz,rho0z,state_z,pars,Ss,Xs,Ys,Zs,alphas,phis)
    %划分单元计算单元各个节点坐标以及各个单元节点对应的长度位置，井斜角，方位角，油管内径，油管外径
    nodes=create_mesh(pars,Ss,Xs,Ys,Zs,alphas,phis);             %划分网格
    %
    nelem=sum(pars.mesh);%节点总数
    Kgg=zeros((nelem+1)*5,(nelem+1)*5);
    Mgg=zeros((nelem+1)*5,(nelem+1)*5);
    Cgg=zeros((nelem+1)*5,(nelem+1)*5);
    Fgravg=zeros((nelem+1)*5,1);
    transmat=cell(nelem,1);
    %
    %循环计算单元刚度质量阻尼矩阵并组装
    %形函数:单元坐标系下节点自由度顺序为：z,x,ry,y,rx
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
    phiz=@(z,le)[1-z/le;0;0;0;0;z/le;0;0;0;0];
    %采用差分方式定义一阶微分 
    scale=0.01;         %差分尺度
    dphix=@(z,le)(phix(z+scale,le)-phix(z-scale,le))/2/scale;
    ddphix=@(z,le)(dphix(z+scale,le)-dphix(z-scale,le))/2/scale;
    dphiy=@(z,le)(phiy(z+scale,le)-phiy(z-scale,le))/2/scale;
    ddphiy=@(z,le)(dphiy(z+scale,le)-dphiy(z-scale,le))/2/scale;
    dphiz=@(z,le)(phiz(z+scale,le)-phiz(z-scale,le))/2/scale;
    ddphiz=@(z,le)(dphiz(z+scale,le)-dphiz(z-scale,le))/2/scale;
%       dphix=@(z,le)[0;-6*z/le^2+6*z^2/le^3;1-4*z/le+3*z^2/le^2;0;0;0;6*z/le^2-6*z^2/le^3;-2*z/le+3*z^2/le^2;0;0];
%       ddphix=@(z,le)[0;-6/le^2+12*z/le^3;-4/le+6*z/le^2;0;0;0;6/le^2-12*z/le^3;-2/le+6*z/le^2;0;0];
%       dphiy=@(z,le)[0;0;0;-6*z/le^2+6*z^2/le^3;1-4*z/le+3*z^2/le^2;0;0;0;6*z/le^2-6*z^2/le^3;-2*z/le+3*z^2/le^2];
%       ddphiy=@(z,le)[0;0;0;-6/le^2+12*z/le^3;-4/le+6*z/le^2;0;0;0;6/le^2-12*z/le^3;-2/le+6*z/le^2];
%       dphiz=@(z,le)[-1/le;0;0;0;0;1/le;0;0;0;0];
%       ddphiz=@(z,le)[0;0;0;0;0;0;0;0;0;0];
    
    for i=1:nelem
        %生成单元坐标系下的质量刚度阻尼矩阵
       [M,K,C,fgrave,elem_transmat,A11,A22,le1,I11,I21]=create_elem_mat_in_local(nodes(i,:),nodes(i+1,:),pars,...
            phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,state_z,rho0z,Vz);
        %组装刚度质量阻尼矩阵
        A1(i)=A11;
        A2(i)=A22;
        le(i)=le1;
        I1(i)=I11;
        I2(i)=I21;
        Kgg(i*5-4:i*5+5,i*5-4:i*5+5)=Kgg(i*5-4:i*5+5,i*5-4:i*5+5)+elem_transmat'*K*elem_transmat;
        Mgg(i*5-4:i*5+5,i*5-4:i*5+5)=Mgg(i*5-4:i*5+5,i*5-4:i*5+5)+elem_transmat'*M*elem_transmat;
        Cgg(i*5-4:i*5+5,i*5-4:i*5+5)=Cgg(i*5-4:i*5+5,i*5-4:i*5+5)+elem_transmat'*C*elem_transmat;
        
%         Fgravg(i*5-4:i*5+5)=Fgravg(i*5-4:i*5+5)+elem_transmat'*fgrave;
                Fgravg(i*5-4:i*5+5)=Fgravg(i*5-4:i*5+5)+fgrave;
        transmat{i}=elem_transmat;
    end
end

function nodes=create_mesh(pars,Ss,Xs,Ys,Zs,alphas,phis)
    nodes=zeros(sum(pars.mesh),9);
    ltemp=0;
    count=2;
    for i=1:numel(pars.mesh)
        le=pars.Ls(i)/pars.mesh(i);         %该分段的单元长度
        for j=1:pars.mesh(i)
            ltemp=ltemp+le;
            x0=interp1(Ss,Xs,ltemp,'spline');
            y0=interp1(Ss,Ys,ltemp,'spline');
            z0=interp1(Ss,Zs,ltemp,'spline');
            alpha0=interp1(Ss,alphas,ltemp,'spline');
            phi0=interp1(Ss,phis,ltemp,'spline'); 
            nodes(count,:)=[x0,y0,z0,ltemp,alpha0,phi0,pars.Rvi(i),pars.Rvo(i),pars.QQ1(i)];
            count=count+1;
        end
    end
end


function [M,K,C,fgrave,elem_transmat,A1,A2,le,I1,I2]=create_elem_mat_in_local(node1,node2,pars,phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,state_z,rho0z,Vz)
    %计算一些参数
    le=norm(node2(1:3)-node1(1:3),2);           %单元长度
    A1=pi*node1(8)^2-pi*node1(7)^2;
    A2=pi*node2(8)^2-pi*node2(7)^2;         %单元两个节点对应截面面积
    I1=pi*node1(8)^4/4-pi*node1(7)^4/4;
    I2=pi*node2(8)^4/4-pi*node2(7)^4/4;     %两个截面的惯性矩
    I=@(z)interp1([0,le],[I1,I2],z);        %油管惯性矩定义为函数
    A=@(z)interp1([0,le],[A1,A2],z);        %油管截面积定义为函数
    ve=1/3*le*(A1+sqrt(A1*A2)+A2);          %体积
    mv=pars.rhov*ve;

    %
    rho0=@(z,le)interp1(state_z,rho0z,node1(3)+(node2(3)-node1(3))*z/le,'spline');     %当前单元位置流体密度，定义为单元轴向坐标系下函数
    Aempty=@(z)interp1([0,le],pi*pars.Rti^2-pi*[node1(8)^2,node2(8)^2],z);       %当前单元位置环空面积定义为线性函数
    m0=quadgk(@(z)rho0(z,le).*Aempty(z),0,le);
    V=quadgk(@(z)Aempty(z),0,le);         %环空体积
    %计算单元质量矩阵
    M1=quadv(@(z)(mv+m0)*phix(z,le)*(phix(z,le))',0,le);       %单元质量矩阵1
    M2=quadv(@(z)(mv+m0)*phiy(z,le)*(phiy(z,le))',0,le);       %单元质量矩阵2
    M3=quadv(@(z)(pars.rhov*I(z))*dphix(z,le)*(dphix(z,le))',0,le);       %单元质量矩阵3
    M4=quadv(@(z)(pars.rhov*I(z))*dphiy(z,le)*(dphiy(z,le))',0,le);       %单元质量矩阵4
    M5=quadv(@(z)mv*phiz(z,le)*(phiz(z,le))',0,le);       %单元质量矩阵5
    M=M1+M2+M3+M4+M5;
    %计算单元阻尼矩阵
    C1=quadv(@(z)pars.c*phix(z,le)*(phix(z,le))',0,le);       %单元阻尼矩阵1
    C2=quadv(@(z)2*m0*V*phix(z,le)*(dphix(z,le))',0,le);       %单元阻尼矩阵2
    C3=quadv(@(z)pars.c*phiy(z,le)*(phiy(z,le))',0,le);       %单元阻尼矩阵3
    C4=quadv(@(z)2*m0*V*phiy(z,le)*(dphiy(z,le))',0,le);       %单元阻尼矩阵4
    C5=quadv(@(z)pars.c*phiz(z,le)*(phiz(z,le))',0,le);       %单元阻尼矩阵5
    C=C1+C2+C3+C4+C5;
    %计算单元刚度矩阵,其他刚度矩阵在迭代中更新
    K1=quadv(@(z)pars.Ev*I(z)*ddphix(z,le)*(ddphix(z,le))',0,le);       %单元刚度矩阵1
    K2=quadv(@(z)pars.Ev*I(z)*ddphiy(z,le)*(ddphiy(z,le))',0,le);       %单元刚度矩阵2
    K3=quadv(@(z)-m0*V^2*dphix(z,le)*(dphix(z,le))',0,le);       %单元刚度矩阵3
    K4=quadv(@(z)-m0*V^2*dphiy(z,le)*(dphiy(z,le))',0,le);       %单元刚度矩阵4
    K11=quadv(@(z)pars.Ev*A(z)*dphiz(z,le)*(dphiz(z,le))',0,le);       %单元刚度矩阵11
    K=K1+K2+K3+K4+K11;
    %计算单元坐标变换矩阵
    %采用单元中部的井斜角和方位角
    alpha=(node1(5)+node2(5))/2;
    phi=(node1(6)+node2(6))/2;
%     T1=[cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0;%%有可能有问题
%         sin(alpha),cos(alpha),0,0,0;
%         0,0,1,0,0;
%         -cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0;
%         0,0,0,0,1];
%     elem_transmat=[cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0,0,0,0,0,0;
%         sin(alpha),cos(alpha),0,0,0,0,0,0,0,0;
%         0,0,1,0,0,0,0,0,0,0;
%         -cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0,0,0,0,0,0;
%         0,0,0,0,1,0,0,0,0,0,;
%         0,0,0,0,0,cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0;
%         0,0,0,0,0,sin(alpha),cos(alpha),0,0,0;
%         0,0,0,0,0,0,0,1,0,0;
%         0,0,0,0,0,-cos(alpha)*sin(phi),sin(alpha)*sin(phi),0,cos(phi),0;
%         0,0,0,0,0,0,0,0,0,1];
     T1=[cos(alpha),-sin(phi)*sin(alpha),0,sin(alpha)*cos(phi),0;
         0,cos(phi),0,sin(phi),0;
         0,0,1,0,0,;
         -sin(alpha),-sin(phi)*cos(alpha),0,cos(alpha)*cos(phi),0;
         0,0,0,0,1];
    elem_transmat=blkdiag(T1,T1); 
    
    
    %重力
    thetad=(node1(5)+node2(5))/2;
    q=quadgk(@(z)(pars.rhov-rho0(z,le)).*A(z)*9.81,0,le);               %单位长度重力
%      q1=q*cos(thetad);         %重力在求解坐标系分量
%      q2=q*sin(thetad);
%      fgrave=-[-q1*le/2,-q2*le/2,0,0,-q2*le^2/12,-q1*le/2,-q2*le/2,0,0,q1*le^2/12]';
    fgrave=[q/2,0,0,0,0,q/2,0,0,0,0]';
%      fgrave=0;
    
end


