def plot_ccd_individual(
        ccd_data, plot_origin=True, mask=None, extract_array_from_mask=False, zoom_around_mask=False, positions=None,
        should_plot_image=False,
        should_plot_noise_map=False,
        should_plot_psf=False,
        should_plot_signal_to_noise_map=False,
        should_plot_absolute_signal_to_noise_map=False,
        should_plot_potential_chi_squared_map=False,
        units='arcsec',
        output_path=None, output_format='png'):
    """Plot each attribute of the ccd data as individual figures one by one (e.g. the data, noise_map-map, PSF, \
     Signal-to_noise-map, etc).

    Set *autolens.data.array.plotters.array_plotters* for a description of all innput parameters not described below.

    Parameters
    -----------
    ccd_data : data.CCDData
        The ccd data, which includes the observed data, noise_map-map, PSF, signal-to-noise_map-map, etc.
    plot_origin : True
        If true, the origin of the data's coordinate system is plotted as a 'x'.
    """

    if should_plot_image:

        plot_image(
            ccd_data=ccd_data, plot_origin=plot_origin, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask, positions=positions,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_noise_map:

        plot_noise_map(
            ccd_data=ccd_data, plot_origin=plot_origin, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_psf:

        plot_psf(
            ccd_data=ccd_data, plot_origin=plot_origin,
            output_path=output_path, output_format=output_format)

    if should_plot_signal_to_noise_map:

        plot_signal_to_noise_map(
            ccd_data=ccd_data, plot_origin=plot_origin, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_absolute_signal_to_noise_map:

        plot_absolute_signal_to_noise_map(
            ccd_data=ccd_data, plot_origin=plot_origin, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)
    
    if should_plot_potential_chi_squared_map:

        plot_potential_chi_squared_map(
            ccd_data=ccd_data, plot_origin=plot_origin, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)