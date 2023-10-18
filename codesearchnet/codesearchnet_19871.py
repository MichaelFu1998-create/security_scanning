def check_AP_phase(abf,n=10):
    """X"""
    timePoints=get_AP_timepoints(abf)[:10] #first 10
    if len(timePoints)==0:
        return
    swhlab.plot.new(abf,True,title="AP phase (n=%d)"%n,xlabel="mV",ylabel="V/S")
    Ys=abf.get_data_around(timePoints,msDeriv=.1,padding=.005)
    Xs=abf.get_data_around(timePoints,padding=.005)
    for i in range(1,len(Ys)):
        pylab.plot(Xs[i],Ys[i],alpha=.2,color='b')
    pylab.plot(Xs[0],Ys[0],alpha=.4,color='r',lw=1)
    pylab.margins(.1,.1)