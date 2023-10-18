def make_analysis(self, positions, pixel_scale, results=None):
        """
        Create an lens object. Also calls the prior passing and lens_data modifying functions to allow child
        classes to change the behaviour of the phase.

        Parameters
        ----------
        pixel_scale
        positions
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens: Analysis
            An lens object that the non-linear optimizer calls to determine the fit of a set of values
        """
        self.pass_priors(results)
        analysis = self.__class__.Analysis(positions=positions, pixel_scale=pixel_scale, cosmology=self.cosmology,
                                           results=results)
        return analysis