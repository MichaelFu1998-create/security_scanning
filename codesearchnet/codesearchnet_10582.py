def make_analysis(self, data, results=None, mask=None, positions=None):
        """
        Create an lens object. Also calls the prior passing and lens_data modifying functions to allow child
        classes to change the behaviour of the phase.

        Parameters
        ----------
        positions
        mask: Mask
            The default masks passed in by the pipeline
        data: im.CCD
            An lens_data that has been masked
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens : Analysis
            An lens object that the non-linear optimizer calls to determine the fit of a set of values
        """

        mask = setup_phase_mask(data=data, mask=mask, mask_function=self.mask_function,
                                inner_mask_radii=self.inner_mask_radii)

        if self.positions_threshold is not None and positions is not None:
            positions = list(map(lambda position_set: np.asarray(position_set), positions))
        elif self.positions_threshold is None:
            positions = None
        elif self.positions_threshold is not None and positions is None:
            raise exc.PhaseException('You have specified for a phase to use positions, but not input positions to the '
                                     'pipeline when you ran it.')

        lens_data = li.LensData(ccd_data=data, mask=mask, sub_grid_size=self.sub_grid_size,
                                image_psf_shape=self.image_psf_shape, positions=positions,
                                interp_pixel_scale=self.interp_pixel_scale)

        modified_image = self.modify_image(image=lens_data.image, results=results)
        lens_data = lens_data.new_lens_data_with_modified_image(modified_image=modified_image)

        if self.bin_up_factor is not None:
            lens_data = lens_data.new_lens_data_with_binned_up_ccd_data_and_mask(bin_up_factor=self.bin_up_factor)

        self.pass_priors(results)

        self.output_phase_info()

        analysis = self.__class__.Analysis(lens_data=lens_data, cosmology=self.cosmology,
                                           positions_threshold=self.positions_threshold, results=results)
        return analysis