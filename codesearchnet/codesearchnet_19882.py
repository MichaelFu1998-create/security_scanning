def comments(abf,minutes=False):
    """draw vertical lines at comment points. Defaults to seconds."""
    if not len(abf.commentTimes):
        return
    for i in range(len(abf.commentTimes)):
        t,c = abf.commentTimes[i],abf.commentTags[i]
        if minutes:
            t=t/60
        pylab.axvline(t,lw=1,color='r',ls="--",alpha=.5)
        X1,X2,Y1,Y2=pylab.axis()
        Y2=Y2-abs(Y2-Y1)*.02
        pylab.text(t,Y2,c,size=8,color='r',rotation='vertical',
                   ha='right',va='top',weight='bold',alpha=.5)
        if minutes:
            pylab.xlabel("minutes")
        else:
            pylab.xlabel("seconds")