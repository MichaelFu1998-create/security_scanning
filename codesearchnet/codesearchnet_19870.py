def check_AP_deriv(abf,n=10):
    """X"""
    timePoints=get_AP_timepoints(abf)[:10] #first 10
    if len(timePoints)==0:
        return
    swhlab.plot.new(abf,True,title="AP velocity (n=%d)"%n,xlabel="ms",ylabel="V/S")
    pylab.axhline(-50,color='r',lw=2,ls="--",alpha=.2)
    pylab.axhline(-100,color='r',lw=2,ls="--",alpha=.2)
    Ys=abf.get_data_around(timePoints,msDeriv=.1,padding=.005)
    Xs=(np.arange(len(Ys[0]))-len(Ys[0])/2)*1000/abf.rate
    for i in range(1,len(Ys)):
        pylab.plot(Xs,Ys[i],alpha=.2,color='b')
    pylab.plot(Xs,Ys[0],alpha=.4,color='r',lw=2)
    pylab.margins(0,.1)