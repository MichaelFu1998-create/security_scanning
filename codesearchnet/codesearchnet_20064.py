def plot_shaded_data(X,Y,variances,varianceX):
    """plot X and Y data, then shade its background by variance."""
    plt.plot(X,Y,color='k',lw=2)
    nChunks=int(len(Y)/CHUNK_POINTS)
    for i in range(0,100,PERCENT_STEP):
        varLimitLow=np.percentile(variances,i)
        varLimitHigh=np.percentile(variances,i+PERCENT_STEP)
        varianceIsAboveMin=np.where(variances>=varLimitLow)[0]
        varianceIsBelowMax=np.where(variances<=varLimitHigh)[0]
        varianceIsRange=[chunkNumber for chunkNumber in range(nChunks) \
                         if chunkNumber in varianceIsAboveMin \
                         and chunkNumber in varianceIsBelowMax]
        for chunkNumber in varianceIsRange:
            t1=chunkNumber*CHUNK_POINTS/POINTS_PER_SEC
            t2=t1+CHUNK_POINTS/POINTS_PER_SEC
            plt.axvspan(t1,t2,alpha=.3,color=COLORMAP(i/100),lw=0)