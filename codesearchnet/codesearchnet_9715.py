def plot_all_stops(g, ax=None, scalebar=False):
    """
    Parameters
    ----------
    g: A gtfspy.gtfs.GTFS object
    ax: matplotlib.Axes object, optional
        If None, a new figure and an axis is created, otherwise results are plotted on the axis.
    scalebar: bool, optional
        Whether to include a scalebar to the plot.

    Returns
    -------
    ax: matplotlib.Axes

    """
    assert(isinstance(g, GTFS))
    lon_min, lon_max, lat_min, lat_max = get_spatial_bounds(g)
    smopy_map = get_smopy_map(lon_min, lon_max, lat_min, lat_max)
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax = smopy_map.show_mpl(figsize=None, ax=ax, alpha=0.8)

    stops = g.stops()
    lats = numpy.array(stops['lat'])
    lons = numpy.array(stops['lon'])

    xs, ys = smopy_map.to_pixels(lats, lons)
    ax.scatter(xs, ys, color="red", s=10)

    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(max(ys), min(ys))
    return ax