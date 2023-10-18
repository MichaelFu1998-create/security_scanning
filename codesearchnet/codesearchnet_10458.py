def plot_fit_individuals_lens_and_source_planes(
        fit, should_plot_mask=True, extract_array_from_mask=False, zoom_around_mask=False, positions=None,
        should_plot_image_plane_pix=False,
        should_plot_image=False,
        should_plot_noise_map=False,
        should_plot_signal_to_noise_map=False,
        should_plot_lens_subtracted_image=False,
        should_plot_model_image=False,
        should_plot_lens_model_image=False,
        should_plot_source_model_image=False,
        should_plot_source_plane_image=False,
        should_plot_residual_map=False,
        should_plot_chi_squared_map=False,
        units='arcsec',
        output_path=None, output_format='show'):
    """Plot the model datas_ of an analysis, using the *Fitter* class object.

    The visualization and output type can be fully customized.

    Parameters
    -----------
    fit : autolens.lens.fitting.Fitter
        Class containing fit between the model datas_ and observed lens datas_ (including residual_map, chi_squared_map etc.)
    output_path : str
        The path where the datas_ is output if the output_type is a file format (e.g. png, fits)
    output_format : str
        How the datas_ is output. File formats (e.g. png, fits) output the datas_ to harddisk. 'show' displays the datas_ \
        in the python interpreter window.
    """

    mask = lens_plotter_util.get_mask(fit=fit, should_plot_mask=should_plot_mask)

    kpc_per_arcsec = fit.tracer.image_plane.kpc_per_arcsec

    if should_plot_image:

        image_plane_pix_grid = lens_plotter_util.get_image_plane_pix_grid(should_plot_image_plane_pix, fit)

        lens_plotter_util.plot_image(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            image_plane_pix_grid=image_plane_pix_grid,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_noise_map:

        lens_plotter_util.plot_noise_map(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_signal_to_noise_map:

        lens_plotter_util.plot_signal_to_noise_map(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_lens_subtracted_image:

        lens_plotter_util.plot_lens_subtracted_image(
            fit=fit, mask=mask, positions=positions, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_model_image:
        lens_plotter_util.plot_model_data(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_lens_model_image:

        lens_plotter_util.plot_model_image_of_planes(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            plot_foreground=True,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_filename='fit_lens_plane_model_image', output_format=output_format)

    if should_plot_source_model_image:

        lens_plotter_util.plot_model_image_of_planes(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            plot_source=True,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_filename='fit_source_plane_model_image', output_format=output_format)

    if should_plot_source_plane_image:

        if fit.total_inversions == 0:

           plane_plotters.plot_plane_image(
               plane=fit.tracer.source_plane, plot_grid=True,
               units=units, figsize=(20, 20),
               output_path=output_path, output_filename='fit_source_plane', output_format=output_format)

        elif fit.total_inversions == 1:

            inversion_plotters.plot_reconstructed_pixelization(
                inversion=fit.inversion, should_plot_grid=True,
                units=units, figsize=(20, 20),
                output_path=output_path, output_filename='fit_source_plane', output_format=output_format)

    if should_plot_residual_map:

        lens_plotter_util.plot_residual_map(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)

    if should_plot_chi_squared_map:

        lens_plotter_util.plot_chi_squared_map(
            fit=fit, mask=mask, extract_array_from_mask=extract_array_from_mask, zoom_around_mask=zoom_around_mask,
            units=units, kpc_per_arcsec=kpc_per_arcsec,
            output_path=output_path, output_format=output_format)