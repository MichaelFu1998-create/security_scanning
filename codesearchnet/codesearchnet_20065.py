def show_variances(Y,variances,varianceX,logScale=False):
    """create some fancy graphs to show color-coded variances."""
    
    plt.figure(1,figsize=(10,7))
    plt.figure(2,figsize=(10,7))
    varSorted=sorted(variances)
    
    plt.figure(1)
    plt.subplot(211)
    plt.grid()
    plt.title("chronological variance")
    plt.ylabel("original data")
    plot_shaded_data(X,Y,variances,varianceX)
    plt.margins(0,.1)   
    plt.subplot(212)
    plt.ylabel("variance (pA) (log%s)"%str(logScale))
    plt.xlabel("time in sweep (sec)")
    plt.plot(varianceX,variances,'k-',lw=2)
    
    plt.figure(2)
    plt.ylabel("variance (pA) (log%s)"%str(logScale))
    plt.xlabel("chunk number")
    plt.title("sorted variance")
    plt.plot(varSorted,'k-',lw=2)
    
    for i in range(0,100,PERCENT_STEP):
        varLimitLow=np.percentile(variances,i)
        varLimitHigh=np.percentile(variances,i+PERCENT_STEP)
        label="%2d-%d percentile"%(i,i++PERCENT_STEP)
        color=COLORMAP(i/100)
        print("%s: variance = %.02f - %.02f"%(label,varLimitLow,varLimitHigh))
        plt.figure(1)
        plt.axhspan(varLimitLow,varLimitHigh,alpha=.5,lw=0,color=color,label=label)
        plt.figure(2)
        chunkLow=np.where(varSorted>=varLimitLow)[0][0]
        chunkHigh=np.where(varSorted>=varLimitHigh)[0][0]
        plt.axvspan(chunkLow,chunkHigh,alpha=.5,lw=0,color=color,label=label)
        
    for fignum in [1,2]:
        plt.figure(fignum)
        if logScale:
            plt.semilogy()
        plt.margins(0,0)
        plt.grid()
        if fignum is 2:
            plt.legend(fontsize=10,loc='upper left',shadow=True)
        plt.tight_layout()
        plt.savefig('2016-12-15-variance-%d-log%s.png'%(fignum,str(logScale)))
    plt.show()