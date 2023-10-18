def run(self, data, results=None, mask=None, positions=None):
        """
        Run a fit for each galaxy from the previous phase.

        Parameters
        ----------
        data: LensData
        results: ResultsCollection
            Results from all previous phases
        mask: Mask
            The mask
        positions

        Returns
        -------
        results: HyperGalaxyResults
            A collection of results, with one item per a galaxy
        """
        model_image = results.last.unmasked_model_image
        galaxy_tuples = results.last.constant.name_instance_tuples_for_class(g.Galaxy)

        results_copy = copy.copy(results.last)

        for name, galaxy in galaxy_tuples:
            optimizer = self.optimizer.copy_with_name_extension(name)
            optimizer.variable.hyper_galaxy = g.HyperGalaxy
            galaxy_image = results.last.unmasked_image_for_galaxy(galaxy)
            optimizer.fit(self.__class__.Analysis(data, model_image, galaxy_image))

            getattr(results_copy.variable, name).hyper_galaxy = optimizer.variable.hyper_galaxy
            getattr(results_copy.constant, name).hyper_galaxy = optimizer.constant.hyper_galaxy

        return results_copy