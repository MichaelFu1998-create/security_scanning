def showfig(fig, aspect="auto"):
    """
    Shows a figure with a typical orientation so that x and y axes are set up as expected.
    """

    ax = fig.gca()

    # Swap y axis if needed
    alim = list(ax.axis())
    if alim[3] < alim[2]:
        temp    = alim[2]
        alim[2] = alim[3]
        alim[3] = temp
        ax.axis(alim)

    ax.set_aspect(aspect)
    fig.show()