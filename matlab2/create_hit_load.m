function FhitG=create_hit_load(Ug,Vg,kh,kh0,cf,miud,miudx,rs,Ri,meshs,trans_mat)
    uy=zeros(sum(meshs)+1,1);
    uz=zeros(sum(meshs)+1,1);
    vx=zeros(sum(meshs)+1,1);
    vy=zeros(sum(meshs)+1,1);
    vz=zeros(sum(meshs)+1,1);
    vt=zeros(sum(meshs)+1,1);
    for i=1:sum(meshs)              %��Ԫ����ϵ�½ṹ��λ��
        R=Ri;    
        Ue=Ug(i*5-4:i*5+5);
        Ve=Vg(i*5-4:i*5+5);
        Ue=trans_mat{i}*Ue;
        Ve=trans_mat{i}*Ve;
        uy(i)=uy(i)+Ue(4);
        uy(i+1)=uy(i+1)+Ue(9);
        uz(i)=uz(i)+Ue(1);
        uz(i+1)=uz(i+1)+Ue(6);
        vx(i)=vx(i)+Ve(2);
        vx(i+1)=vx(i+1)+Ve(7);
        vy(i)=vy(i)+Ve(4);
        vy(i+1)=vy(i+1)+Ve(9);
        vz(i)=vz(i)+Ve(1);
        vz(i+1)=vz(i+1)+Ve(6);
        vt(i)=0;
        vt(i+1)=0;
    end
    uy(2:end-1)=uy(2:end-1)/2;
    uz(2:end-1)=uz(2:end-1)/2;
    vx(2:end-1)=vx(2:end-1)/2;
    vy(2:end-1)=vy(2:end-1)/2;
    vz(2:end-1)=vz(2:end-1)/2;
    vt(2:end-1)=vt(2:end-1)/2;
    ur=sqrt(uy.^2+uz.^2);
    dur=sqrt(vy.^2+vz.^2);
    %���������⾶����
    r=zeros(size(uy));
    r(1)=rs(1);
    count=1;
    for i=1:numel(meshs)
        r(count+1:count+meshs(i))=rs(i);
        count=count+meshs(i);
    end
    Ff=zeros(size(vy));
    Fy=Ff;
    Fz=Ff;                                       %��ʼ��
    Fx=Ff;
    cosall=[uy,uz].*[vy,vz];
    cosall=(cosall(:,1)+cosall(:,2))./ur;
    Fn=(-(ur+r-R)*kh-dur*cf.*cosall).*(ur+r-R>=0);       %������ײ�غ�
    Fn(1)=(-(ur(1)+r(1)-R(1))*kh0-dur(1)*cf.*cosall(1)).*(ur(1)+r(1)-R(1)>=0);        %�ײ�Լ���غ�
    loc=find(ur+r-R>=0);
    if numel(loc)~=0
       Ff(loc)=-abs(miud*Fn(loc)).*sign(vt(loc));                        %����Ħ����
       Fx(loc)=-abs(miudx*Fn(loc)).*sign(vx(loc));
       Fy(loc)=Fn(loc).*uy(loc)./(uy(loc).^2+uz(loc).^2)+Ff(loc).*uz(loc)./(uy(loc).^2+uz(loc).^2);
       Fz(loc)=Fn(loc).*uz(loc)./(uy(loc).^2+uz(loc).^2)+Ff(loc).*uy(loc)./(uy(loc).^2+uz(loc).^2);                   %��ײ������ 
    end
    Fhit=zeros(size(Ug));               %��Ԫ����ϵ��Լ����
    Fhit(2:5:end)=Fx;
    Fhit(4:5:end)=Fy;
    Fhit(1:5:end)=Fz;
    
    %��ײĦ������Ч�غ�
    FhitG=zeros(size(Fhit));            %����ȫ��������Լ����
    for i=1:sum(meshs)
        Fe=Fhit(i*5-4:i*5+5);
        Fhit(i*5-4:i*5+5)=0;            %ת������0
        FhitG(i*5-4:i*5+5)=FhitG(i*5-4:i*5+5)+(trans_mat{i})'*Fe;
    end
    
    
    
end