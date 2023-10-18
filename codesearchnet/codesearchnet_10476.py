def plot_array(array, origin=None, mask=None, extract_array_from_mask=False, zoom_around_mask=False,
               should_plot_border=False, positions=None, centres=None, axis_ratios=None, phis=None, grid=None,
               as_subplot=False,
               units='arcsec', kpc_per_arcsec=None, figsize=(7, 7), aspect='equal',
               cmap='jet', norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
               cb_ticksize=10, cb_fraction=0.047, cb_pad=0.01, cb_tick_values=None, cb_tick_labels=None,
               title='Array', titlesize=16, xlabelsize=16, ylabelsize=16, xyticksize=16,
               mask_pointsize=10, border_pointsize=2, position_pointsize=30, grid_pointsize=1,
               xticks_manual=None, yticks_manual=None,
               output_path=None, output_format='show', output_filename='array'):
    """Plot an array of data as a figure.

    Parameters
    -----------
    array : data.array.scaled_array.ScaledArray
        The 2D array of data which is plotted.
    origin : (float, float).
        The origin of the coordinate system of the array, which is plotted as an 'x' on the image if input.
    mask : data.array.mask.Mask
        The mask applied to the array, the edge of which is plotted as a set of points over the plotted array.
    extract_array_from_mask : bool
        The plotter array is extracted using the mask, such that masked values are plotted as zeros. This ensures \
        bright features outside the mask do not impact the color map of the plot.
    zoom_around_mask : bool
        If True, the 2D region of the array corresponding to the rectangle encompassing all unmasked values is \
        plotted, thereby zooming into the region of interest.
    should_plot_border : bool
        If a mask is supplied, its borders pixels (e.g. the exterior edge) is plotted if this is *True*.
    positions : [[]]
        Lists of (y,x) coordinates on the image which are plotted as colored dots, to highlight specific pixels.
    grid : data.array.grids.RegularGrid
        A grid of (y,x) coordinates which may be plotted over the plotted array.
    as_subplot : bool
        Whether the array is plotted as part of a subplot, in which case the grid figure is not opened / closed.
    units : str
        The units of the y / x axis of the plots, in arc-seconds ('arcsec') or kiloparsecs ('kpc').
    kpc_per_arcsec : float or None
        The conversion factor between arc-seconds and kiloparsecs, required to plot the units in kpc.
    figsize : (int, int)
        The size of the figure in (rows, columns).
    aspect : str
        The aspect ratio of the array, specifically whether it is forced to be square ('equal') or adapts its size to \
        the figure size ('auto').
    cmap : str
        The colormap the array is plotted using, which may be chosen from the standard matplotlib colormaps.
    norm : str
        The normalization of the colormap used to plot the image, specifically whether it is linear ('linear'), log \
        ('log') or a symmetric log normalization ('symmetric_log').
    norm_min : float or None
        The minimum array value the colormap map spans (all values below this value are plotted the same color).
    norm_max : float or None
        The maximum array value the colormap map spans (all values above this value are plotted the same color).
    linthresh : float
        For the 'symmetric_log' colormap normalization ,this specifies the range of values within which the colormap \
        is linear.
    linscale : float
        For the 'symmetric_log' colormap normalization, this allowws the linear range set by linthresh to be stretched \
        relative to the logarithmic range.
    cb_ticksize : int
        The size of the tick labels on the colorbar.
    cb_fraction : float
        The fraction of the figure that the colorbar takes up, which resizes the colorbar relative to the figure.
    cb_pad : float
        Pads the color bar in the figure, which resizes the colorbar relative to the figure.
    xlabelsize : int
        The fontsize of the x axes label.
    ylabelsize : int
        The fontsize of the y axes label.
    xyticksize : int
        The font size of the x and y ticks on the figure axes.
    mask_pointsize : int
        The size of the points plotted to show the mask.
    border_pointsize : int
        The size of the points plotted to show the borders.
    positions_pointsize : int
        The size of the points plotted to show the input positions.
    grid_pointsize : int
        The size of the points plotted to show the grid.
    xticks_manual :  [] or None
        If input, the xticks do not use the array's default xticks but instead overwrite them as these values.
    yticks_manual :  [] or None
        If input, the yticks do not use the array's default yticks but instead overwrite them as these values.
    output_path : str
        The path on the hard-disk where the figure is output.
    output_filename : str
        The filename of the figure that is output.
    output_format : str
        The format the figue is output:
        'show' - display on computer screen.
        'png' - output to hard-disk as a png.
        'fits' - output to hard-disk as a fits file.'

    Returns
    --------
    None

    Examples
    --------
        array_plotters.plot_array(
        array=image, origin=(0.0, 0.0), mask=circular_mask, extract_array_from_mask=True, zoom_around_mask=True,
        should_plot_border=False, positions=[[1.0, 1.0], [2.0, 2.0]], grid=None, as_subplot=False,
        units='arcsec', kpc_per_arcsec=None, figsize=(7,7), aspect='auto',
        cmap='jet', norm='linear, norm_min=None, norm_max=None, linthresh=None, linscale=None,
        cb_ticksize=10, cb_fraction=0.047, cb_pad=0.01, cb_tick_values=None, cb_tick_labels=None,
        title='Image', titlesize=16, xlabelsize=16, ylabelsize=16, xyticksize=16,
        mask_pointsize=10, border_pointsize=2, position_pointsize=10, grid_pointsize=10,
        xticks_manual=None, yticks_manual=None,
        output_path='/path/to/output', output_format='png', output_filename='image')
    """

    if array is None:
        return

    if extract_array_from_mask and mask is not None:
        array = np.add(array, 0.0, out=np.zeros_like(array), where=np.asarray(mask) == 0)

    if zoom_around_mask and mask is not None:
        array = array.zoomed_scaled_array_around_mask(mask=mask, buffer=2)
        zoom_offset_pixels = np.asarray(mask.zoom_offset_pixels)
        zoom_offset_arcsec = np.asarray(mask.zoom_offset_arcsec)
    else:
        zoom_offset_pixels = None
        zoom_offset_arcsec = None

    if aspect is 'square':
        aspect = float(array.shape_arcsec[1]) / float(array.shape_arcsec[0])

    fig = plot_figure(array=array, as_subplot=as_subplot, units=units, kpc_per_arcsec=kpc_per_arcsec,
            figsize=figsize, aspect=aspect, cmap=cmap, norm=norm,
                norm_min=norm_min, norm_max=norm_max, linthresh=linthresh, linscale=linscale,
                xticks_manual=xticks_manual, yticks_manual=yticks_manual)

    plotter_util.set_title(title=title, titlesize=titlesize)
    set_xy_labels_and_ticksize(units=units, kpc_per_arcsec=kpc_per_arcsec, xlabelsize=xlabelsize, ylabelsize=ylabelsize,
                               xyticksize=xyticksize)

    set_colorbar(cb_ticksize=cb_ticksize, cb_fraction=cb_fraction, cb_pad=cb_pad,
                 cb_tick_values=cb_tick_values, cb_tick_labels=cb_tick_labels)
    plot_origin(array=array, origin=origin, units=units, kpc_per_arcsec=kpc_per_arcsec,
                zoom_offset_arcsec=zoom_offset_arcsec)
    plot_mask(mask=mask, units=units, kpc_per_arcsec=kpc_per_arcsec, pointsize=mask_pointsize,
              zoom_offset_pixels=zoom_offset_pixels)
    plot_border(mask=mask, should_plot_border=should_plot_border, units=units, kpc_per_arcsec=kpc_per_arcsec,
                pointsize=border_pointsize, zoom_offset_pixels=zoom_offset_pixels)
    plot_points(points_arcsec=positions, array=array, units=units, kpc_per_arcsec=kpc_per_arcsec,
                pointsize=position_pointsize, zoom_offset_arcsec=zoom_offset_arcsec)
    plot_grid(grid_arcsec=grid, array=array, units=units, kpc_per_arcsec=kpc_per_arcsec, pointsize=grid_pointsize,
              zoom_offset_arcsec=zoom_offset_arcsec)
    plot_centres(array=array, centres=centres, units=units, kpc_per_arcsec=kpc_per_arcsec,
                zoom_offset_arcsec=zoom_offset_arcsec)
    plot_ellipses(fig=fig, array=array, centres=centres, axis_ratios=axis_ratios, phis=phis, units=units,
                  kpc_per_arcsec=kpc_per_arcsec, zoom_offset_arcsec=zoom_offset_arcsec)
    plotter_util.output_figure(array, as_subplot=as_subplot, output_path=output_path, output_filename=output_filename,
                               output_format=output_format)
    plotter_util.close_figure(as_subplot=as_subplot)