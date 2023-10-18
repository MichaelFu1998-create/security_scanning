def fit_lens_data_with_sensitivity_tracers(lens_data, tracer_normal, tracer_sensitive):
    """Fit lens data with a normal tracer and sensitivity tracer, to determine our sensitivity to a selection of \ 
    galaxy components. This factory automatically determines the type of fit based on the properties of the galaxies \
    in the tracers.

    Parameters
    -----------
    lens_data : lens_data.LensData or lens_data.LensDataHyper
        The lens-images that is fitted.
    tracer_normal : ray_tracing.AbstractTracer
        A tracer whose galaxies have the same model components (e.g. light profiles, mass profiles) as the \
        lens data that we are fitting.
    tracer_sensitive : ray_tracing.AbstractTracerNonStack
        A tracer whose galaxies have the same model components (e.g. light profiles, mass profiles) as the \
        lens data that we are fitting, but also addition components (e.g. mass clumps) which we measure \
        how sensitive we are too.
    """

    if (tracer_normal.has_light_profile and tracer_sensitive.has_light_profile) and \
            (not tracer_normal.has_pixelization and not tracer_sensitive.has_pixelization):
        return SensitivityProfileFit(lens_data=lens_data, tracer_normal=tracer_normal,
                                     tracer_sensitive=tracer_sensitive)

    elif (not tracer_normal.has_light_profile and not tracer_sensitive.has_light_profile) and \
            (tracer_normal.has_pixelization and tracer_sensitive.has_pixelization):
        return SensitivityInversionFit(lens_data=lens_data, tracer_normal=tracer_normal,
                                     tracer_sensitive=tracer_sensitive)
    else:

        raise exc.FittingException('The sensitivity_fit routine did not call a SensitivityFit class - check the '
                                   'properties of the tracers')