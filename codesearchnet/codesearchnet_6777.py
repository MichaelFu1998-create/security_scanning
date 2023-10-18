def main_derivatives_and_departures(T, P, V, b, delta, epsilon, a_alpha,
                                        da_alpha_dT, d2a_alpha_dT2, quick=True):
        '''Re-implementation of derivatives and excess property calculations, 
        as ZeroDivisionError errors occur with the general solution. The 
        following derivation is the source of these formulas.
        
        >>> from sympy import *
        >>> P, T, V, R, b, a = symbols('P, T, V, R, b, a')
        >>> P_vdw = R*T/(V-b) - a/(V*V)
        >>> vdw = P_vdw - P
        >>> 
        >>> dP_dT = diff(vdw, T)
        >>> dP_dV = diff(vdw, V)
        >>> d2P_dT2 = diff(vdw, T, 2)
        >>> d2P_dV2 = diff(vdw, V, 2)
        >>> d2P_dTdV = diff(vdw, T, V)
        >>> H_dep = integrate(T*dP_dT - P_vdw, (V, oo, V))
        >>> H_dep += P*V - R*T
        >>> S_dep = integrate(dP_dT - R/V, (V,oo,V))
        >>> S_dep += R*log(P*V/(R*T))
        >>> Cv_dep = T*integrate(d2P_dT2, (V,oo,V))
        >>> 
        >>> dP_dT, dP_dV, d2P_dT2, d2P_dV2, d2P_dTdV, H_dep, S_dep, Cv_dep
        (R/(V - b), -R*T/(V - b)**2 + 2*a/V**3, 0, 2*(R*T/(V - b)**3 - 3*a/V**4), -R/(V - b)**2, P*V - R*T - a/V, R*(-log(V) + log(V - b)) + R*log(P*V/(R*T)), 0)
        '''
        dP_dT = R/(V - b)
        dP_dV = -R*T/(V - b)**2 + 2*a_alpha/V**3
        d2P_dT2 = 0
        d2P_dV2 = 2*(R*T/(V - b)**3 - 3*a_alpha/V**4)
        d2P_dTdV = -R/(V - b)**2
        H_dep = P*V - R*T - a_alpha/V
        S_dep = R*(-log(V) + log(V - b)) + R*log(P*V/(R*T))
        Cv_dep = 0
        return [dP_dT, dP_dV, d2P_dT2, d2P_dV2, d2P_dTdV, H_dep, S_dep, Cv_dep]