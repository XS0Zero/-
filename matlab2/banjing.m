function  [Rt,rt,It]=banjing(C)
 t=numel(C(:,1));
 ltrans=zeros(t,1);
 dtrans=zeros(t,1);
 Dtrans=zeros(t,1);
 for i=1:t
  ltrans(i)=round(C(i,3)); 
  dtrans(i)=C(i,1);
  Dtrans(i)=C(i,2);
 end
 I=pi*(Dtrans(1)^4-dtrans(1)^4)/64;                                  % �����Ծ�
 %%
 %������������
 %�����ϲ���
 Ntrans=numel(Dtrans);                   %�����ص�����������
 nntrans=zeros(Ntrans,1);               %��nntrans��ǰn���ۼ�
 ntrans=sum(ltrans);                     %�����ص��������ܳ������㲽����
 Rt=zeros(ntrans,1);                     %������������뾶/m
 rt=zeros(ntrans,1);                     %�����������ڰ뾶/m
 Aot=zeros(ntrans,1);                    %����������������/m^2
Ait=zeros(ntrans,1);                    %�����������ڽ����/m^2
It=zeros(ntrans,1);                     %���Ծ�
ht=zeros(ntrans,1);                     %�ں�
%����nnntrans�����ں�������
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%���������ϸ��ֶεİ뾶�������������
for i=1:Ntrans
    if i==1
        for j=1:nntrans(i)
            Rt(j)=Dtrans(i)/2;  
            rt(j)=dtrans(i)/2;
            Aot(j)=pi*Rt(j)^2;
            Ait(j)=pi*rt(j)^2;
            It(j)=pi*(Rt(j)^4-rt(j)^4)/4;
            ht(j)=Rt(j)-rt(j);
        end
    else
        for j=nntrans(i-1)+1:nntrans(i)
            Rt(j)=Dtrans(i)/2;
            rt(j)=dtrans(i)/2;
            Aot(j)=pi*Rt(j).^2;
            Ait(j)=pi*rt(j).^2;
            It(j)=pi*(Rt(j)^4-rt(j)^4)/4;
            ht(j)=Rt(j)-rt(j);
        end
    end
end
end