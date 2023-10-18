def plot_model_image_of_planes(
        fit, plot_foreground=False, plot_source=False, mask=None, extract_array_from_mask=False, zoom_around_mask=False,
        positions=None, plot_mass_profile_centres=True, as_subplot=False,
        units='arcsec', kpc_per_arcsec=None, figsize=(7, 7), aspect='square',
        cmap='jet', norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
        cb_ticksize=10, cb_fraction=0.047, cb_pad=0.01, cb_tick_values=None, cb_tick_labels=None,
        title='Fit Model Image', titlesize=16, xlabelsize=16, ylabelsize=16, xyticksize=16,
        mask_pointsize=10, position_pointsize=10,
        output_path=None, output_format='show', output_filename='fit_model_image_of_plane'):
    """Plot the model image of a specific plane of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    plane_indexes : [int]
        The plane from which the model image is generated.
    """

    centres = get_mass_profile_centes(plot_mass_profile_centres=plot_mass_profile_centres, fit=fit)

    if plot_foreground:

        if fit.tracer.total_planes == 2:
            model_image = fit.model_image_of_planes[0]
        else:
            model_image = sum(fit.model_image_of_planes[0:-2])

    elif plot_source:

        model_image = fit.model_image_of_planes[-1]

    else:

        raise exc.PlottingException('Both plot_foreground and plot_source were False, one must be True')

    array_plotters.plot_array(
        array=model_image, mask=mask, extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask, positions=positions, centres=centres, as_subplot=as_subplot,
        units=units, kpc_per_arcsec=kpc_per_arcsec, figsize=figsize, aspect=aspect,
        cmap=cmap, norm=norm, norm_min=norm_min, norm_max=norm_max, linthresh=linthresh, linscale=linscale,
        cb_ticksize=cb_ticksize, cb_fraction=cb_fraction, cb_pad=cb_pad, 
        cb_tick_values=cb_tick_values, cb_tick_labels=cb_tick_labels,
        title=title, titlesize=titlesize, xlabelsize=xlabelsize, ylabelsize=ylabelsize, xyticksize=xyticksize,
        mask_pointsize=mask_pointsize, position_pointsize=position_pointsize,
        output_path=output_path, output_format=output_format, output_filename=output_filename)