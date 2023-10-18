def axesfontsize(ax, fontsize):
    """
    Change the font size for the title, x and y labels, and x and y tick labels for axis *ax* to *fontsize*.
    """
    items = ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels())
    for item in items:
        item.set_fontsize(fontsize)