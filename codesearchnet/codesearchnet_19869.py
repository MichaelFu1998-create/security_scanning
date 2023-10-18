def check_AP_raw(abf,n=10):
    """X"""
    timePoints=get_AP_timepoints(abf)[:n] #first 10
    if len(timePoints)==0:
        return
    swhlab.plot.new(abf,True,title="AP shape (n=%d)"%n,xlabel="ms")
    Ys=abf.get_data_around(timePoints,padding=.2)
    Xs=(np.arange(len(Ys[0]))-len(Ys[0])/2)*1000/abf.rate
    for i in range(1,len(Ys)):
        pylab.plot(Xs,Ys[i],alpha=.2,color='b')
    pylab.plot(Xs,Ys[0],alpha=.4,color='r',lw=2)
    pylab.margins(0,.1)
    msg=cm.msgDict(cm.dictFlat(abf.APs)[0],cantEndWith="I")
    pylab.subplots_adjust(right=0.7)
    pylab.annotate(msg,(.71,.95),ha='left',va='top',
                   xycoords='figure fraction',family='monospace',size=10)