function  [rt]=banjing1(C)
 t=numel(C(:,1));
 ltrans=zeros(t,1);
 dtrans=zeros(t,1);
 for i=1:t
  ltrans(i)=round(C(i,2)); 
  dtrans(i)=C(i,1);
 end
 %%
 %基础参数输入
 %钻具组合参数
 Ntrans=numel(dtrans);                   %所加载的钻具组合数量
 nntrans=zeros(Ntrans,1);               %即nntrans的前n项累加
 ntrans=sum(ltrans);                     %所加载的钻具组合总长（计算步长）
 rt=zeros(ntrans,1);                     %各段钻具组合内半径/m
%计算nnntrans，便于后续计算
nntrans(1)=ltrans(1);
for i=2:Ntrans
    nntrans(i)=nntrans(i-1)+ltrans(i);
end
%计算钻具组合各分段的半径、截面积、线重
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