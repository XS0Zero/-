import numpy as np
    
def fatiguelife(dxyl = None,jsd2 = None,QQ1 = None): 
    for p in np.arange(1,jsd2+1).reshape(-1):
        Load = np.transpose(dxyl(p,:))
        Load1 = Load
        Load2 = Load
        L3 = len(Load2)
        #����ѭ�������������ֲο�SAE ASTM��׼
        ## ����һ ##
        #���غ�ʱ�����̽��д���ʹ��ֻ������ȷ�Ƚ������
        m1 = L3
        for i in np.arange(2,m1 - 1+1,1).reshape(-1):
            if Load2(i - 1) <= Load2(i) and Load2(i) <= Load2(i + 1):
                Load1[i] = NaN
            else:
                if Load2(i - 1) >= Load2(i) and Load2(i) >= Load2(i + 1):
                    Load1[i] = NaN
        Load1[np.isnan[Load1]] = []
        ## ����� ##
        #���غ�ʱ���������죬ʹ�����С��ֵ�𿪣�ǰ��ƴ�ӣ�ʹ����ֵ��ʼ��ֵ����
        a,b = np.amax(Load1)
        n1 = len(Load1)
        B1 = Load1(np.arange(b,n1+1))
        B2 = Load1(np.arange(1,b+1))
        Load1 = np.array([[B1],[B2]])
        ## ������ ##
        #��ֻ�����岨�ȣ���ֹƴ�Ӵ����ֲ����������
        Load2 = Load1
        m1 = len(Load1)
        for i in np.arange(2,m1 - 1+1,1).reshape(-1):
            if Load2(i - 1) < Load2(i) and Load2(i) < Load2(i + 1):
                Load1[i] = NaN
            else:
                if Load2(i - 1) > Load2(i) and Load2(i) > Load2(i + 1):
                    Load1[i] = NaN
        Load1[np.isnan[Load1]] = []
        n1 = len(Load1)
        # BΪ������غ�ʱ������  nΪB�в��岨�ȵĸ���
        ## ������ ##
        #��������������  1��ֵF 2��ֵJ  ��������ѭ��ģʽ
        Amplitude = []
        Mean = []
        while len(Load1) >= 1:

            n1 = len(Load1)
            if n1 == 1 or n1 == 2:
                break
            else:
                if n1 > 2:
                    for j in np.arange(1,n1 - 2+1).reshape(-1):
                        s1 = np.abs(Load1(j + 1) - Load1(j))
                        s2 = np.abs(Load1(j + 1) - Load1(j + 2))
                        e3 = (Load1(j + 1) + Load1(j + 2)) / 2
                        if s1 <= s2:
                            Amplitude = np.array([[Amplitude],[s1]])
                            Mean = np.array([[Mean],[e3]])
                            Load1[j] = []
                            Load1[j] = []
                            n1 = len(Load1)
                            break
                        else:
                            continue
            continue

        D1 = Load1
        ## ������ ##
        #��ͼ�� ��άhist��άͼ��
        X = np.array([Mean,Amplitude])
        ##########################################
        ss21 = np.zeros((len(Amplitude),1))
        for i in np.arange(1,len(Amplitude)+1).reshape(-1):
            ss21[i] = Amplitude(i) / (1 - Mean(i) / QQ1(p))
        for i in np.arange(1,len(ss21)+1).reshape(-1):
            N[i] = (1.845 * 1e+17 / (np.exp(0.04 * ss21(i)))) / 10 ** 8
            #    N(i)=((ss21(i)/1000000/2513.6).^(-7.57578));
#      N(i)=(4441.1/ss21(i))^0.161;
#     N(i)=(ss21(i)./1000000/2513.6).^(-7.57578);   #SN����
# N(i)=(exp(2.7202-log(ss21(i))))^(1/0.05851);
# N(i)=(((exp(2.7202)/ss21(i))^(0.05851)))*10^10;
        N = np.transpose(N)
        for i in np.arange(1,len(ss21)+1).reshape(-1):
            fatigue1[i] = 1 / N(i)
        fatigue2 = sum(fatigue1)
        fatigue333[p] = 1 / fatigue2
    
    fatigue33 = (real(fatigue333)) / 3
    fatigue332 = fatigue33 + mean(fatigue33)
    # if p==1
#    fatigue33(p)=fatigue33(p)*10^4;
# elseif p==2
#    fatigue33(p)=fatigue33(p)*10^4;
# else
# end
    
    return fatigue332
    
    return fatigue332