function fatigue332=fatiguelife(dxyl,jsd2,QQ1)
for p=1:jsd2
Load=dxyl(p,:)';
Load1=Load;Load2=Load;
L3=length(Load2);
%三点循环计数法；部分参考SAE ASTM标准

%% 步骤一 %%

%对载荷时间历程进行处理使它只包含峰谷峰谷交替出现

m1=L3;

for i=2:1:m1-1

    if Load2(i-1)<=Load2(i)&&Load2(i)<=Load2(i+1)

        Load1(i)=NaN;

    elseif Load2(i-1)>=Load2(i)&&Load2(i)>=Load2(i+1)

        Load1(i)=NaN;

    end

end

Load1(isnan(Load1))=[];

%% 步骤二 %%

%对载荷时间历程再造，使从最大（小）值拆开，前后拼接，使从最值开始最值结束

[a,b]=max(Load1);

n1=length(Load1);

B1=Load1(b:n1);

B2=Load1(1:b);

Load1=[B1;B2];

%% 步骤三 %%

%再只留波峰波谷，防止拼接处出现不合理的数据

Load2=Load1;m1=length(Load1);

for i=2:1:m1-1

    if Load2(i-1)<Load2(i)&&Load2(i)<Load2(i+1)

        Load1(i)=NaN;

    elseif Load2(i-1)>Load2(i)&&Load2(i)>Load2(i+1)

        Load1(i)=NaN;

    end

end

Load1(isnan(Load1))=[];n1=length(Load1);

% B为改造后载荷时间历程  n为B中波峰波谷的个数

%% 步骤四 %%

%雨流计数记因素  1幅值F 2均值J  开启无脑循环模式

Amplitude=[];Mean=[];

while length(Load1)>=1

    n1=length(Load1);

    if n1==1||n1==2

        break

    elseif n1>2

        for j=1:n1-2

            s1=abs(Load1(j+1)-Load1(j));

            s2=abs(Load1(j+1)-Load1(j+2));

            e3=(Load1(j+1)+Load1(j+2))/2;

            if s1<=s2

                Amplitude=[Amplitude;s1];

                Mean=[Mean;e3];

                Load1(j)=[];

                Load1(j)=[];

                n1=length(Load1);

                break;

            else

                continue;

            end

        end

    end

    continue

end

D1=Load1;

%% 步骤五 %%

%画图像 三维hist三维图像

X=[Mean,Amplitude];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ss21=zeros(length(Amplitude),1);
for i=1:length(Amplitude)
 ss21(i)=Amplitude(i)/(1-Mean(i)/QQ1(p));
end
for i=1:length(ss21)
   N(i)=(1.845*10E16/(exp(0.04*ss21(i))))/10^8;
%    N(i)=((ss21(i)/1000000/2513.6).^(-7.57578)); 
%      N(i)=(4441.1/ss21(i))^0.161;
%     N(i)=(ss21(i)./1000000/2513.6).^(-7.57578);   %SN曲线
% N(i)=(exp(2.7202-log(ss21(i))))^(1/0.05851);
% N(i)=(((exp(2.7202)/ss21(i))^(0.05851)))*10^10;
end
N=N';
for i=1:length(ss21)
     fatigue1(i)=1/N(i);
end
fatigue2=sum(fatigue1);
fatigue333(p)=1/fatigue2;
end
fatigue33=(real(fatigue333))/3;
fatigue332=fatigue33+mean(fatigue33);
% if p==1
%    fatigue33(p)=fatigue33(p)*10^4; 
% elseif p==2
%    fatigue33(p)=fatigue33(p)*10^4; 
% else
% end

end