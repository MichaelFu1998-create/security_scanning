def figureStimulus(abf,sweeps=[0]):
    """
    Create a plot of one area of interest of a single sweep.
    """

    stimuli=[2.31250, 2.35270]
    for sweep in sweeps:
        abf.setsweep(sweep)
        for stimulus in stimuli:
            S1=int(abf.pointsPerSec*stimulus)
            S2=int(abf.pointsPerSec*(stimulus+0.001)) # 1ms of blanking
            abf.sweepY[S1:S2]=np.nan # blank out the stimulus area
        I1=int(abf.pointsPerSec*2.2) # time point (sec) to start
        I2=int(abf.pointsPerSec*2.6) # time point (sec) to end
        baseline=np.average(abf.sweepY[int(abf.pointsPerSec*2.0):int(abf.pointsPerSec*2.2)])
        Ys=lowPassFilter(abf.sweepY[I1:I2])-baseline
        Xs=abf.sweepX2[I1:I1+len(Ys)].flatten()
        plt.plot(Xs,Ys,alpha=.5,lw=2)
    return