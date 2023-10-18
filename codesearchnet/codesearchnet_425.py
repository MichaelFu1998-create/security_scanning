def configure_legend(ax, autofmt_xdate=True, change_colors=False,
                     rotation=30, ha='right'):
    """
    Format legend for perf attribution plots:
    - put legend to the right of plot instead of overlapping with it
    - make legend order match up with graph lines
    - set colors according to colormap
    """
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0,
                     chartBox.width * 0.75, chartBox.height])

    # make legend order match graph lines
    handles, labels = ax.get_legend_handles_labels()
    handles_and_labels_sorted = sorted(zip(handles, labels),
                                       key=lambda x: x[0].get_ydata()[-1],
                                       reverse=True)

    handles_sorted = [h[0] for h in handles_and_labels_sorted]
    labels_sorted = [h[1] for h in handles_and_labels_sorted]

    if change_colors:
        for handle, color in zip(handles_sorted,
                                 cycle(COLORS)):

            handle.set_color(color)

    ax.legend(handles=handles_sorted,
              labels=labels_sorted,
              frameon=True,
              framealpha=0.5,
              loc='upper left',
              bbox_to_anchor=(1.05, 1),
              fontsize='large')

    # manually rotate xticklabels instead of using matplotlib's autofmt_xdate
    # because it disables xticklabels for all but the last plot
    if autofmt_xdate:
        for label in ax.get_xticklabels():
            label.set_ha(ha)
            label.set_rotation(rotation)