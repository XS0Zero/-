function  [rt]=banjing1(C)
 t=numel(C(:,1));
 ltrans=zeros(t,1);
 dtrans=zeros(t,1);
 for i=1:t
  ltrans(i)=round(C(i,2)); 
  dtrans(i)=C(i,1);
 end
 %%
 %������������
 %�����ϲ���
 Ntrans=numel(dtrans);                   %�����ص�����������
 nntrans=zeros(Ntrans,1);               %��nntrans��ǰn���ۼ�
 ntrans=sum(ltrans);                     %�����ص��������ܳ������㲽����
 rt=zeros(ntrans,1);                     %�����������ڰ뾶/m
%����nnntrans�����ں�������
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%���������ϸ��ֶεİ뾶�������������
for i=1:Ntrans
    if i==1
        for j=1:nntrans(i) 
            rt(j)=dtrans(i)/2;
        end
    else
        for j=nntrans(i-1)+1:nntrans(i)
            rt(j)=dtrans(i)/2;
        end
    end
end

end