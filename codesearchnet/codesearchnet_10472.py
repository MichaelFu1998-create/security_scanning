def plot_ray_tracing_individual(
        tracer, mask=None, extract_array_from_mask=False, zoom_around_mask=False, positions=None,
        should_plot_image_plane_image=False,
        should_plot_source_plane=False,
        should_plot_convergence=False,
        should_plot_potential=False,
        should_plot_deflections=False,
        units='arcsec',
        output_path=None, output_format='show'):
    """Plot the observed _tracer of an analysis, using the *CCD* class object.

    The visualization and output type can be fully customized.

    Parameters
    -----------
    tracer : autolens.ccd.tracer.CCD
        Class containing the _tracer, noise_map-mappers and PSF that are to be plotted.
        The font size of the figure ylabel.
    output_path : str
        The path where the _tracer is output if the output_type is a file format (e.g. png, fits)
    output_format : str
        How the _tracer is output. File formats (e.g. png, fits) output the _tracer to harddisk. 'show' displays the _tracer \
        in the python interpreter window.
    """

    if should_plot_image_plane_image:

        plot_image_plane_image(
            tracer=tracer, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask, positions=positions,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_convergence:

        plot_convergence(
            tracer=tracer, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_potential:

        plot_potential(
            tracer=tracer, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_source_plane:

        plane_plotters.plot_plane_image(
            plane=tracer.source_plane, positions=None, plot_grid=False,
            units=units,
            output_path=output_path, output_filename='tracer_source_plane', output_format=output_format)

    if should_plot_deflections:

        plot_deflections_y(
            tracer=tracer, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)

    if should_plot_deflections:

        plot_deflections_x(
            tracer=tracer, mask=mask, extract_array_from_mask=extract_array_from_mask,
            zoom_around_mask=zoom_around_mask,
            units=units,
            output_path=output_path, output_format=output_format)