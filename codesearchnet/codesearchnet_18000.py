def lbl(axis, label, size=22):
    """ Put a figure label in an axis """
    at = AnchoredText(label, loc=2, prop=dict(size=size), frameon=True)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.0")
    #bb = axis.get_yaxis_transform()
    #at = AnchoredText(label,
    #        loc=3, prop=dict(size=18), frameon=True,
    #        bbox_to_anchor=(-0.5,1),#(-.255, 0.90),
    #        bbox_transform=bb,#axis.transAxes
    #    )
    axis.add_artist(at)