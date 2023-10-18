def unique_cpx_roots(rlist,tol = 0.001):
    """
    
    The average of the root values is used when multiplicity 
    is greater than one.

    Mark Wickert October 2016
    """
    uniq = [rlist[0]]
    mult = [1]
    for k in range(1,len(rlist)):
        N_uniq = len(uniq)
        for m in range(N_uniq):
            if abs(rlist[k]-uniq[m]) <= tol:
                mult[m] += 1
                uniq[m] = (uniq[m]*(mult[m]-1) + rlist[k])/float(mult[m])
                break
        uniq = np.hstack((uniq,rlist[k]))
        mult = np.hstack((mult,[1]))
    return np.array(uniq), np.array(mult)