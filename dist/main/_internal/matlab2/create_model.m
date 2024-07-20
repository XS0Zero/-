function [Mgg,Kgg,Cgg,Fgravg,transmat,nodes,A1,A2,le,I1,I2]=create_model(Vz,rho0z,state_z,pars,Ss,Xs,Ys,Zs,alphas,phis)
    %���ֵ�Ԫ���㵥Ԫ�����ڵ������Լ�������Ԫ�ڵ��Ӧ�ĳ���λ�ã���б�ǣ���λ�ǣ��͹��ھ����͹��⾶
    nodes=create_mesh(pars,Ss,Xs,Ys,Zs,alphas,phis);             %��������
    %
    nelem=sum(pars.mesh);%�ڵ�����
    Kgg=zeros((nelem+1)*5,(nelem+1)*5);
    Mgg=zeros((nelem+1)*5,(nelem+1)*5);
    Cgg=zeros((nelem+1)*5,(nelem+1)*5);
    Fgravg=zeros((nelem+1)*5,1);
    transmat=cell(nelem,1);
    %
    %ѭ�����㵥Ԫ�ն��������������װ
    %�κ���:��Ԫ����ϵ�½ڵ����ɶ�˳��Ϊ��z,x,ry,y,rx
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
    %���ò�ַ�ʽ����һ��΢�� 
    scale=0.01;         %��ֳ߶�
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
        %���ɵ�Ԫ����ϵ�µ������ն��������
       [M,K,C,fgrave,elem_transmat,A11,A22,le1,I11,I21]=create_elem_mat_in_local(nodes(i,:),nodes(i+1,:),pars,...
            phix,phiy,phiz,dphix,dphiy,dphiz,ddphix,ddphiy,ddphiz,state_z,rho0z,Vz);
        %��װ�ն������������
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
        le=pars.Ls(i)/pars.mesh(i);         %�÷ֶεĵ�Ԫ����
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
    %����һЩ����
    le=norm(node2(1:3)-node1(1:3),2);           %��Ԫ����
    A1=pi*node1(8)^2-pi*node1(7)^2;
    A2=pi*node2(8)^2-pi*node2(7)^2;         %��Ԫ�����ڵ��Ӧ�������
    I1=pi*node1(8)^4/4-pi*node1(7)^4/4;
    I2=pi*node2(8)^4/4-pi*node2(7)^4/4;     %��������Ĺ��Ծ�
    I=@(z)interp1([0,le],[I1,I2],z);        %�͹ܹ��Ծض���Ϊ����
    A=@(z)interp1([0,le],[A1,A2],z);        %�͹ܽ��������Ϊ����
    ve=1/3*le*(A1+sqrt(A1*A2)+A2);          %���
    mv=pars.rhov*ve;

    %
    rho0=@(z,le)interp1(state_z,rho0z,node1(3)+(node2(3)-node1(3))*z/le,'spline');     %��ǰ��Ԫλ�������ܶȣ�����Ϊ��Ԫ��������ϵ�º���
    Aempty=@(z)interp1([0,le],pi*pars.Rti^2-pi*[node1(8)^2,node2(8)^2],z);       %��ǰ��Ԫλ�û����������Ϊ���Ժ���
    m0=quadgk(@(z)rho0(z,le).*Aempty(z),0,le);
    V=quadgk(@(z)Aempty(z),0,le);         %�������
    %���㵥Ԫ��������
    M1=quadv(@(z)(mv+m0)*phix(z,le)*(phix(z,le))',0,le);       %��Ԫ��������1
    M2=quadv(@(z)(mv+m0)*phiy(z,le)*(phiy(z,le))',0,le);       %��Ԫ��������2
    M3=quadv(@(z)(pars.rhov*I(z))*dphix(z,le)*(dphix(z,le))',0,le);       %��Ԫ��������3
    M4=quadv(@(z)(pars.rhov*I(z))*dphiy(z,le)*(dphiy(z,le))',0,le);       %��Ԫ��������4
    M5=quadv(@(z)mv*phiz(z,le)*(phiz(z,le))',0,le);       %��Ԫ��������5
    M=M1+M2+M3+M4+M5;
    %���㵥Ԫ�������
    C1=quadv(@(z)pars.c*phix(z,le)*(phix(z,le))',0,le);       %��Ԫ�������1
    C2=quadv(@(z)2*m0*V*phix(z,le)*(dphix(z,le))',0,le);       %��Ԫ�������2
    C3=quadv(@(z)pars.c*phiy(z,le)*(phiy(z,le))',0,le);       %��Ԫ�������3
    C4=quadv(@(z)2*m0*V*phiy(z,le)*(dphiy(z,le))',0,le);       %��Ԫ�������4
    C5=quadv(@(z)pars.c*phiz(z,le)*(phiz(z,le))',0,le);       %��Ԫ�������5
    C=C1+C2+C3+C4+C5;
    %���㵥Ԫ�նȾ���,�����նȾ����ڵ����и���
    K1=quadv(@(z)pars.Ev*I(z)*ddphix(z,le)*(ddphix(z,le))',0,le);       %��Ԫ�նȾ���1
    K2=quadv(@(z)pars.Ev*I(z)*ddphiy(z,le)*(ddphiy(z,le))',0,le);       %��Ԫ�նȾ���2
    K3=quadv(@(z)-m0*V^2*dphix(z,le)*(dphix(z,le))',0,le);       %��Ԫ�նȾ���3
    K4=quadv(@(z)-m0*V^2*dphiy(z,le)*(dphiy(z,le))',0,le);       %��Ԫ�նȾ���4
    K11=quadv(@(z)pars.Ev*A(z)*dphiz(z,le)*(dphiz(z,le))',0,le);       %��Ԫ�նȾ���11
    K=K1+K2+K3+K4+K11;
    %���㵥Ԫ����任����
    %���õ�Ԫ�в��ľ�б�Ǻͷ�λ��
    alpha=(node1(5)+node2(5))/2;
    phi=(node1(6)+node2(6))/2;
%     T1=[cos(alpha)*cos(phi),-cos(phi)*sin(alpha),0,sin(phi),0;%%�п���������
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
    
    
    %����
    thetad=(node1(5)+node2(5))/2;
    q=quadgk(@(z)(pars.rhov-rho0(z,le)).*A(z)*9.81,0,le);               %��λ��������
%      q1=q*cos(thetad);         %�������������ϵ����
%      q2=q*sin(thetad);
%      fgrave=-[-q1*le/2,-q2*le/2,0,0,-q2*le^2/12,-q1*le/2,-q2*le/2,0,0,q1*le^2/12]';
    fgrave=[q/2,0,0,0,0,q/2,0,0,0,0]';
%      fgrave=0;
    
end


