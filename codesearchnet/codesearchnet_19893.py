def proto_unknown(theABF):
    """protocol: unknown."""
    abf=ABF(theABF)
    abf.log.info("analyzing as an unknown protocol")
    plot=ABFplot(abf)
    plot.rainbow=False
    plot.title=None
    plot.figure_height,plot.figure_width=SQUARESIZE,SQUARESIZE
    plot.kwargs["lw"]=.5
    plot.figure_chronological()
    plt.gca().set_axis_bgcolor('#AAAAAA') # different background if unknown protocol
    frameAndSave(abf,"UNKNOWN")