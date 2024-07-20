import numpy as np
    
def ququcd(fs = None,fh = None,TAi1 = None,ntrans = None): 
    KS = np.zeros((ntrans,1))
    KH = np.zeros((ntrans,1))
    for i in np.arange(1,ntrans+1).reshape(-1):
        if TAi1(i) < fs(i) and TAi1(i) > fh(i):
            KS[i] = TAi1(i)
        else:
            KS[i] = 0
    
    for i in np.arange(1,ntrans+1).reshape(-1):
        if TAi1(i) <= fh(i):
            KH[i] = TAi1(i)
        else:
            KH[i] = 0
    
    Locs = find(KS < 0)
    
    Loch = find(KH < 0)
    
    return Loch,Locs
    
    return Loch,Locs