function Kggadd=create_timevary_stiff(Ugt,transmat,nodes,pars)
    %计算时变刚度矩阵
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
    %采用差分方式定义一阶微分,二阶微分
    scale=0.01;         %差分尺度
    dphix=@(z,le)(phix(z+scale,le)-phix(z-scale,le))/2/scale;
    ddphix=@(z,le)(dphix(z+scale,le)-dphix(z-scale,le))/2/scale;
    dphiy=@(z,le)(phiy(z+scale,le)-phiy(z-scale,le))/2/scale;
    ddphiy=@(z,le)(dphiy(z+scale,le)-dphiy(z-scale,le))/2/scale;
    dphiz=@(z,le)(phiz(z+scale,le)-phiz(z-scale,le))/2/scale;
    ddphiz=@(z,le)(dphiz(z+scale,le)-dphiz(z-scale,le))/2/scale;
    nelem=sum(pars.mesh);
    Kggadd=zeros((nelem+1)*5,(nelem+1)*5);
    for i=1:nelem
        Kadd=create_elem_timevary_stiff_in_local(nodes(i,:),nodes(i+1,:),pars,...
            phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,Ugt(i*5-4:i*5+5),transmat{i});
        %组装附加刚度矩阵
        Kggadd(i*5-4:i*5+5,i*5-4:i*5+5)=Kggadd(i*5-4:i*5+5,i*5-4:i*5+5)+transmat{i}'*Kadd*transmat{i};
    end
end

function Kadd=create_elem_timevary_stiff_in_local(node1,node2,pars,...
            phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,Uet,elem_transmat)
    %
    %计算一些参数
    le=norm(node2(1:3)-node1(1:3),2);           %单元长度
    A1=pi*node1(8)^2-pi*node1(7)^2;
    A2=pi*node2(8)^2-pi*node2(7)^2;         %单元两个节点对应截面面积
    I1=pi*node1(8)^4/4-pi*node1(7)^4/4;
    I2=pi*node2(8)^4/4-pi*node2(7)^4/4;     %两个截面的惯性矩
    I=@(z)interp1([0,le],[I1,I2],z);        %油管惯性矩定义为函数
    A=@(z)interp1([0,le],[A1,A2],z);        %油管截面积定义为函数
    uet=elem_transmat*Uet;                  %单元坐标系下单元位移向量
    K5=quadv(@(z)pars.Ev*A(z)*dphix(z,le)*uet'*(dphiz(z,le))*(phix(z,le))',0,le);       %单元刚度矩阵5
    K6=quadv(@(z)pars.Ev*A(z)*dphiy(z,le)*uet'*(dphiz(z,le))*(dphiy(z,le))',0,le);       %单元刚度矩阵6
    K7=quadv(@(z)1/2*pars.Ev*A(z)*dphix(z,le)*(dphix(z,le))'*uet*uet'*phix(z,le)*(phix(z,le))',0,le);   %单元刚度矩阵7
    K8=quadv(@(z)1/2*pars.Ev*A(z)*dphiy(z,le)*(dphiy(z,le))'*uet*uet'*dphiy(z,le)*(dphiy(z,le))',0,le); %单元刚度矩阵8
    K9=quadv(@(z)1/2*pars.Ev*A(z)*dphix(z,le)*(dphix(z,le))'*uet*uet'*dphiy(z,le)*(dphiy(z,le))',0,le); %单元刚度矩阵9
    K10=quadv(@(z)1/2*pars.Ev*A(z)*dphiy(z,le)*(dphiy(z,le))'*uet*uet'*dphix(z,le)*(dphix(z,le))',0,le);%单元刚度矩阵10
    K12=quadv(@(z)1/2*pars.Ev*A(z)*dphiz(z,le)*(dphix(z,le))'*uet*(dphix(z,le))',0,le);%单元刚度矩阵12
    K13=quadv(@(z)1/2*pars.Ev*A(z)*dphiz(z,le)*(dphiy(z,le))'*uet*(dphiy(z,le))',0,le);%单元刚度矩阵13
    Kadd=K5+K6+K7+K8+K9+K10+K12+K13;
    
end
