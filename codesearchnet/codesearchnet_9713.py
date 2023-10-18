def plot_as_routes(route_shapes, ax=None, spatial_bounds=None, map_alpha=0.8, plot_scalebar=True, legend=True,
                   return_smopy_map=False, line_width_attribute=None, line_width_scale=1.0, map_style=None):
    """
    Parameters
    ----------
    route_shapes: list of dicts that should have the following keys
            name, type, agency, lats, lons
            with types
            list, list, str, list, list
    ax: axis object
    spatial_bounds: dict
    map_alpha:
    plot_scalebar: bool
    legend:
    return_smopy_map:
    line_width_attribute:
    line_width_scale:

    Returns
    -------
    ax: matplotlib.axes object
    """
    lon_min = spatial_bounds['lon_min']
    lon_max = spatial_bounds['lon_max']
    lat_min = spatial_bounds['lat_min']
    lat_max = spatial_bounds['lat_max']
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    smopy_map = get_smopy_map(lon_min, lon_max, lat_min, lat_max, map_style=map_style)
    ax = smopy_map.show_mpl(figsize=None, ax=ax, alpha=map_alpha)
    bound_pixel_xs, bound_pixel_ys = smopy_map.to_pixels(numpy.array([lat_min, lat_max]),
                                                         numpy.array([lon_min, lon_max]))

    route_types_to_lines = {}
    for shape in route_shapes:
        route_type = ROUTE_TYPE_CONVERSION[shape['type']]
        lats = numpy.array(shape['lats'])
        lons = numpy.array(shape['lons'])
        if line_width_attribute:
            line_width = line_width_scale * shape[line_width_attribute]
        else:
            line_width = 1
        xs, ys = smopy_map.to_pixels(lats, lons)
        line, = ax.plot(xs, ys, linewidth=line_width, color=ROUTE_TYPE_TO_COLOR[route_type], zorder=ROUTE_TYPE_TO_ZORDER[route_type])
        route_types_to_lines[route_type] = line

    if legend:
        lines = list(route_types_to_lines.values())
        labels = [ROUTE_TYPE_TO_SHORT_DESCRIPTION[route_type] for route_type in route_types_to_lines.keys()]
        ax.legend(lines, labels, loc="upper left")

    if plot_scalebar:
        _add_scale_bar(ax, lat_max, lon_min, lon_max, bound_pixel_xs.max() - bound_pixel_xs.min())

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim(bound_pixel_xs.min(), bound_pixel_xs.max())
    ax.set_ylim(bound_pixel_ys.max(), bound_pixel_ys.min())
    if return_smopy_map:
        return ax, smopy_map
    else:
        return ax