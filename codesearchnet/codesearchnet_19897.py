def proto_0202(theABF):
    """protocol: MTIV."""
    abf=ABF(theABF)
    abf.log.info("analyzing as MTIV")
    plot=ABFplot(abf)
    plot.figure_height,plot.figure_width=SQUARESIZE,SQUARESIZE
    plot.title=""
    plot.kwargs["alpha"]=.6
    plot.figure_sweeps()

    # frame to uppwer/lower bounds, ignoring peaks from capacitive transients
    abf.setsweep(0)
    plt.axis([None,None,abf.average(.9,1)-100,None])
    abf.setsweep(-1)
    plt.axis([None,None,None,abf.average(.9,1)+100])

    # save it
    plt.tight_layout()
    frameAndSave(abf,"MTIV")
    plt.close('all')