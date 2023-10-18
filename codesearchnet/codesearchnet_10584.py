def make_analysis(self, galaxy_data, results=None, mask=None):
        """
        Create an lens object. Also calls the prior passing and lens_data modifying functions to allow child
        classes to change the behaviour of the phase.

        Parameters
        ----------
        galaxy_data
        mask: Mask
            The default masks passed in by the pipeline
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens: Analysis
            An lens object that the non-linear optimizer calls to determine the fit of a set of values
        """

        mask = setup_phase_mask(data=galaxy_data[0], mask=mask, mask_function=self.mask_function,
                                inner_mask_radii=None)

        self.pass_priors(results)

        if self.use_intensities or self.use_convergence or self.use_potential:

            galaxy_data = gd.GalaxyFitData(galaxy_data=galaxy_data[0], mask=mask, sub_grid_size=self.sub_grid_size,
                                           use_intensities=self.use_intensities,
                                           use_convergence=self.use_convergence,
                                           use_potential=self.use_potential,
                                           use_deflections_y=self.use_deflections,
                                           use_deflections_x=self.use_deflections)

            return self.__class__.AnalysisSingle(galaxy_data=galaxy_data,
                                                 cosmology=self.cosmology,
                                                 results=results)

        elif self.use_deflections:

            galaxy_data_y = gd.GalaxyFitData(galaxy_data=galaxy_data[0], mask=mask, sub_grid_size=self.sub_grid_size,
                                             use_intensities=self.use_intensities,
                                             use_convergence=self.use_convergence,
                                             use_potential=self.use_potential,
                                             use_deflections_y=self.use_deflections, use_deflections_x=False)

            galaxy_data_x = gd.GalaxyFitData(galaxy_data=galaxy_data[1], mask=mask, sub_grid_size=self.sub_grid_size,
                                             use_intensities=self.use_intensities,
                                             use_convergence=self.use_convergence,
                                             use_potential=self.use_potential,
                                             use_deflections_y=False, use_deflections_x=self.use_deflections)

            return self.__class__.AnalysisDeflections(galaxy_data_y=galaxy_data_y, galaxy_data_x=galaxy_data_x,
                                                      cosmology=self.cosmology,
                                                      results=results)