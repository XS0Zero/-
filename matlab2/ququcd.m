function [Loch,Locs]=ququcd(fs,fh,TAi1,ntrans) 
 
KS=zeros(ntrans,1);
KH=zeros(ntrans,1);

for i=1:ntrans
    if TAi1(i)<fs(i) && TAi1(i)>fh(i)
        KS(i)=TAi1(i);
    else
        KS(i)=0;
    end
end
for i=1:ntrans
    if TAi1(i)<=fh(i)
        KH(i)=TAi1(i);
    else
        KH(i)=0;
    end
end
Locs=find(KS<0);  %取出正弦屈曲的位置
Loch=find(KH<0);  %取出螺旋屈曲的位置
end