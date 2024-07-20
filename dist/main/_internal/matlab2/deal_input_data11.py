import numpy as np
    
def deal_input_data11(data1 = None): 
    data = data1
    Xs = np.zeros((data.shape[1-1],1))
    Ys = np.zeros((data.shape[1-1],1))
    Zs = np.zeros((data.shape[1-1],1))
    alphas = data(:,2) / 180 * np.pi
    
    phis = data(:,3) / 180 * np.pi
    
    Length = np.zeros((data.shape[1-1],1))
    Length = data(:,1)
    for i in np.arange(2,len(Xs)+1).reshape(-1):
        alpha1 = data(i - 1,2) / 180 * np.pi
        alpha2 = data(i,2) / 180 * np.pi
        phi1 = data(i - 1,3) / 180 * np.pi
        phi2 = data(i,3) / 180 * np.pi
        ds = data(i,1) - data(i - 1,1)
        if alpha1 != alpha2 and phi1 != phi2:
            dx = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            dy = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        else:
            if alpha1 == alpha2 and phi1 != phi2:
                dx = ds * np.sin(alpha1) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
                dy = ds * np.sin(alpha1) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
                dz = ds * np.cos(alpha1)
            else:
                if alpha1 != alpha2 and phi1 == phi2:
                    dx = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.cos(phi1)
                    dy = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.sin(phi1)
                    dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
                else:
                    dx = ds * np.sin(alpha1) * np.cos(phi1)
                    dy = ds * np.sin(alpha1) * np.sin(phi1)
                    dz = ds * np.cos(alpha1)
        Xs[i] = Xs(i - 1) + dx
        Ys[i] = Ys(i - 1) + dy
        Zs[i] = Zs(i - 1) + dz
    
    return Length,Xs,Ys,Zs,alphas,phis
    
    return Length,Xs,Ys,Zs,alphas,phis