def fit_exp(y,graphToo=False):
    """Exponential fit. Returns [multiplier, t, offset, time constant]"""
    x=np.arange(len(y))
    try:
        params, cv = scipy.optimize.curve_fit(algo_exp, x, y, p0=(1,1e-6,1))
    except:
        print(" !! curve fit failed (%.02f points)"%len(x))
        return np.nan,np.nan,np.nan,np.nan #can't fit so little data!
    m,t,b=params
    tau=1/t
    if graphToo:
        pylab.figure(figsize=(6,4))
        pylab.grid()
        pylab.title("FIT ASSESSMENT")
        pylab.plot(x,y,'o',mfc='none',ms=10)
        pylab.plot(x,algo_exp(x,m,t,b),'b-',lw=2)
        pylab.show()
    return m,t,b,tau