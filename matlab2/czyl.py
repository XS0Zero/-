import numpy as np
    
def czyl(pars = None,Vz = None,rho0z = None,Tz = None,Ss = None,Zs = None,alphas = None): 
    dV = np.diff(Vz)
    rho0z1 = rho0z * 0.318
    # drho0z=diff(rho0z);
    g = 9.8
    for i in np.arange(1,(len(Tz) - 1)+1).reshape(-1):
        zup1 = interp1(Ss,Zs,i)
        Tei = pars.Tint1 + pars.DT * zup1
        Re = rho0z(i) * Vz(i) * 2 * pars.Rvi(1) / pars.miu
        f = 1 / ((4 * np.log(pars.im / (2 * 3.715 * pars.Rvi(1)) + (6.943 / Re) ** 0.9) ** 2))
        dpdzfr = f * rho0z1(i) * Vz(i) ** 2 / 2 / pars.Rvi(1)
        alpha = interp1(Ss,alphas,zup1)
        dp[i] = - (rho0z1(i) * g * np.cos(alpha) + dpdzfr - rho0z1(i) * Vz(i) * (dV(i)))
        dT[i] = (- ((g * np.cos(alpha) - Vz(i) * (dV(i)) + 2 * np.pi * pars.Rmax * pars.ke * pars.Ua * (Tz(i) - Tei) / (pars.wi * (pars.ke + pars.Rmax * pars.Ua * pars.ft))) / pars.cp)) * 1.06
    
    for i in np.arange(1,(len(Tz))+1).reshape(-1):
        if i == 1:
            paz[1] = pars.pint
            TTT[1] = pars.Tint
        else:
            if i == 2:
                paz[2] = pars.pint + dp(1)
                TTT[2] = pars.Tint + dT(1)
            else:
                paz[i] = paz(i - 1) + dp(i - 1)
                TTT[i] = TTT(i - 1) + dT(i - 1)
    
    pzz = flipud(np.transpose(paz))
    TTT1 = np.transpose(flipud(np.transpose(TTT)))
    return pzz,TTT1
    
    return pzz,TTT1