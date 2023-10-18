def plot_grid(grid, axis_limits=None, points=None, as_subplot=False,
              units='arcsec', kpc_per_arcsec=None,
              figsize=(12, 8), pointsize=5, pointcolor='k', xyticksize=16,
              title='Grid', titlesize=16, xlabelsize=16, ylabelsize=16,
              output_path=None, output_format='show', output_filename='grid'):
    """Plot a grid of (y,x) Cartesian coordinates as a scatter plot of points.

    Parameters
    -----------
    grid : data.array.grids.RegularGrid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2).
    axis_limits : []
        The axis limits of the figure on which the grid is plotted, following [xmin, xmax, ymin, ymax].
    points : []
        A set of points that are plotted in a different colour for emphasis (e.g. to show the mappings between \
        different planes).
    as_subplot : bool
        Whether the grid is plotted as part of a subplot, in which case the grid figure is not opened / closed.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    figsize : (int, int)
        The size of the figure in (rows, columns).
    pointsize : int
        The size of the points plotted on the grid.
    xyticksize : int
        The font size of the x and y ticks on the figure axes.
    title : str
        The text of the title.
    titlesize : int
        The size of of the title of the figure.
    xlabelsize : int
        The fontsize of the x axes label.
    ylabelsize : int
        The fontsize of the y axes label.
    output_path : str
        The path on the hard-disk where the figure is output.
    output_filename : str
        The filename of the figure that is output.
    output_format : str
        The format the figue is output:
        'show' - display on computer screen.
        'png' - output to hard-disk as a png.
    """

    plotter_util.setup_figure(figsize=figsize, as_subplot=as_subplot)
    grid = convert_grid_units(grid_arcsec=grid, units=units, kpc_per_arcsec=kpc_per_arcsec)
    plt.scatter(y=np.asarray(grid[:, 0]), x=np.asarray(grid[:, 1]), s=pointsize, marker='.')
    plotter_util.set_title(title=title, titlesize=titlesize)
    set_xy_labels(units, kpc_per_arcsec, xlabelsize, ylabelsize, xyticksize)

    set_axis_limits(axis_limits)
    plot_points(grid, points, pointcolor)

    plt.tick_params(labelsize=xyticksize)
    plotter_util.output_figure(None, as_subplot, output_path, output_filename, output_format)
    plotter_util.close_figure(as_subplot=as_subplot)