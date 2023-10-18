def proto_0201(theABF):
    """protocol: membrane test."""
    abf=ABF(theABF)
    abf.log.info("analyzing as a membrane test")
    plot=ABFplot(abf)
    plot.figure_height,plot.figure_width=SQUARESIZE/2,SQUARESIZE/2
    plot.figure_sweeps()

    # save it
    plt.tight_layout()
    frameAndSave(abf,"membrane test")
    plt.close('all')