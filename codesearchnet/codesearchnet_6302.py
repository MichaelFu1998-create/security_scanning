def summary(self, solution=None, threshold=1E-06, fva=None, names=False,
                floatfmt='.3g'):
        """
        Print a summary of the input and output fluxes of the model.

        Parameters
        ----------
        solution: cobra.Solution, optional
            A previously solved model solution to use for generating the
            summary. If none provided (default), the summary method will
            resolve the model. Note that the solution object must match the
            model, i.e., changes to the model such as changed bounds,
            added or removed reactions are not taken into account by this
            method.
        threshold : float, optional
            Threshold below which fluxes are not reported.
        fva : pandas.DataFrame, float or None, optional
            Whether or not to include flux variability analysis in the output.
            If given, fva should either be a previous FVA solution matching
            the model or a float between 0 and 1 representing the
            fraction of the optimum objective to be searched.
        names : bool, optional
            Emit reaction and metabolite names rather than identifiers (default
            False).
        floatfmt : string, optional
            Format string for floats (default '.3g').

        """
        from cobra.flux_analysis.summary import model_summary
        return model_summary(self, solution=solution, threshold=threshold,
                             fva=fva, names=names, floatfmt=floatfmt)