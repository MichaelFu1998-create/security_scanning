def for_data_and_tracer(cls, lens_data, tracer, padded_tracer=None):
        """Fit lens data with a model tracer, automatically determining the type of fit based on the \
        properties of the galaxies in the tracer.

        Parameters
        -----------
        lens_data : lens_data.LensData or lens_data.LensDataHyper
            The lens-images that is fitted.
        tracer : ray_tracing.TracerNonStack
            The tracer, which describes the ray-tracing and strong lens configuration.
        padded_tracer : ray_tracing.Tracer or None
            A tracer with an identical strong lens configuration to the tracer above, but using the lens data's \
            padded grid_stack such that unmasked model-images can be computed.
        """

        if tracer.has_light_profile and not tracer.has_pixelization:
            return LensProfileFit(lens_data=lens_data, tracer=tracer, padded_tracer=padded_tracer)
        elif not tracer.has_light_profile and tracer.has_pixelization:
            return LensInversionFit(lens_data=lens_data, tracer=tracer, padded_tracer=None)
        elif tracer.has_light_profile and tracer.has_pixelization:
            return LensProfileInversionFit(lens_data=lens_data, tracer=tracer, padded_tracer=None)
        else:
            raise exc.FittingException('The fit routine did not call a Fit class - check the '
                                       'properties of the tracer')