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
 I=pi*(Dtrans(1)^4-dtrans(1)^4)/64;                                  % 极惯性矩
 %%
 %基础参数输入
 %钻具组合参数
 Ntrans=numel(Dtrans);                   %所加载的钻具组合数量
 nntrans=zeros(Ntrans,1);               %即nntrans的前n项累加
 ntrans=sum(ltrans);                     %所加载的钻具组合总长（计算步长）
 Rt=zeros(ntrans,1);                     %各段钻具组合外半径/m
 rt=zeros(ntrans,1);                     %各段钻具组合内半径/m
 Aot=zeros(ntrans,1);                    %各段钻具组合外截面积/m^2
Ait=zeros(ntrans,1);                    %各段钻具组合内截面积/m^2
It=zeros(ntrans,1);                     %惯性矩
ht=zeros(ntrans,1);                     %壁厚
%计算nnntrans，便于后续计算
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%计算钻具组合各分段的半径、截面积、线重
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