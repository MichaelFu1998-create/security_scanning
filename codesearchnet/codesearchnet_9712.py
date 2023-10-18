def plot_route_network_from_gtfs(g, ax=None, spatial_bounds=None, map_alpha=0.8, scalebar=True, legend=True,
                                 return_smopy_map=False, map_style=None):
    """
    Parameters
    ----------
    g: A gtfspy.gtfs.GTFS object
        Where to get the data from?
    ax: matplotlib.Axes object, optional
        If None, a new figure and an axis is created
    spatial_bounds: dict, optional
        with str keys: lon_min, lon_max, lat_min, lat_max
    return_smopy_map: bool, optional
        defaulting to false

    Returns
    -------
    ax: matplotlib.axes.Axes

    """
    assert(isinstance(g, GTFS))
    route_shapes = g.get_all_route_shapes()

    if spatial_bounds is None:
        spatial_bounds = get_spatial_bounds(g, as_dict=True)
    if ax is not None:
        bbox = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        spatial_bounds = _expand_spatial_bounds_to_fit_axes(spatial_bounds, width, height)
    return plot_as_routes(route_shapes,
                          ax=ax,
                          spatial_bounds=spatial_bounds,
                          map_alpha=map_alpha,
                          plot_scalebar=scalebar,
                          legend=legend,
                          return_smopy_map=return_smopy_map,
                          map_style=map_style)