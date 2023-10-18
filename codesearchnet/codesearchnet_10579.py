def run(self, positions, pixel_scale, results=None):
        """
        Run this phase.

        Parameters
        ----------
        pixel_scale
        positions
        results: autofit.tools.pipeline.ResultsCollection
            An object describing the results of the last phase or None if no phase has been executed

        Returns
        -------
        result: AbstractPhase.Result
            A result object comprising the best fit model and other hyper.
        """
        analysis = self.make_analysis(positions=positions, pixel_scale=pixel_scale, results=results)
        result = self.run_analysis(analysis)
        return self.make_result(result, analysis)